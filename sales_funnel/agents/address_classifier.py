from __future__ import annotations

import asyncio

from sales_funnel.agents.base import BaseAgent
from sales_funnel.models.schemas import (
    AgentResult,
    Company,
    CompanyHealth,
    Lead,
    TopicAffinity,
    TopicRelevance,
)
from sales_funnel.services.llm import LLMService
from sales_funnel.services.search import SearchService


class AddressClassifier(BaseAgent):
    """Agent 2: Klassifiziert Unternehmen nach (A) Firmengesundheit/Aktivität
    und (B) Affinität für ein bestimmtes Software-Thema."""

    name = "address_classifier"

    def __init__(
        self,
        topic: str = "",
        llm: LLMService | None = None,
        search: SearchService | None = None,
        max_concurrent: int = 5,
    ):
        self.topic = topic
        self.llm = llm or LLMService()
        self.search = search or SearchService()
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def run(self, input_data: AgentResult | dict | None = None) -> AgentResult:
        leads = self._extract_leads(input_data)
        topic = self.topic or (
            input_data.metadata.get("topic", "") if isinstance(input_data, AgentResult) else ""
        )

        if not topic:
            raise ValueError("Kein Thema (topic) angegeben für die Klassifizierung")

        tasks = [self._classify_lead(lead, topic) for lead in leads]
        classified = await asyncio.gather(*tasks, return_exceptions=True)

        result_leads = []
        for item in classified:
            if isinstance(item, Lead):
                result_leads.append(item)

        result_leads.sort(
            key=lambda l: l.topic_relevance.combined_score if l.topic_relevance else 0,
            reverse=True,
        )

        return AgentResult(
            agent_name=self.name,
            leads=result_leads,
            metadata={
                "topic": topic,
                "classified_count": len(result_leads),
                "tokens": {
                    "input": self.llm.total_input_tokens,
                    "output": self.llm.total_output_tokens,
                },
            },
        )

    async def _classify_lead(self, lead: Lead, topic: str) -> Lead:
        async with self._semaphore:
            company = lead.company

            # Zwei parallele Suchen: Firmengesundheit + Themen-Affinität
            health_query = f'"{company.name}" news OR Pressemitteilung OR Quartalsbericht'
            topic_query = f'"{company.name}" {topic} news OR Projekt OR Partnerschaft'

            health_results, topic_results = await asyncio.gather(
                self.search.search(health_query, num_results=5),
                self.search.search(topic_query, num_results=5),
            )

            # Dimension A: Firmengesundheit / Aktivität
            health_text = "\n".join(
                f"- {r.title}: {r.snippet}" for r in health_results
            ) or "Keine aktuellen Nachrichten gefunden."

            health = await self.llm.structured_query(
                system=(
                    "Du bist ein B2B-Analyst. Bewerte anhand von Nachrichten und "
                    "Pressemitteilungen, wie es der Firma geht und wie aktiv sie ist. "
                    "Eine aktive Firma mit positiven News bekommt einen hohen Score."
                ),
                prompt=(
                    f"Unternehmen: {company.name}\n"
                    f"Website: {company.website or 'unbekannt'}\n"
                    f"Branche: {company.industry or 'unbekannt'}\n\n"
                    f"Aktuelle Nachrichten:\n{health_text}\n\n"
                    "Bewerte die Aktivität und Gesundheit der Firma (0.0-1.0)."
                ),
                response_model=CompanyHealth,
            )

            # Dimension B: Themen-Affinität
            topic_text = "\n".join(
                f"- {r.title}: {r.snippet}" for r in topic_results
            ) or "Keine themenrelevanten Nachrichten gefunden."

            affinity = await self.llm.structured_query(
                system=(
                    "Du bist ein B2B-Analyst. Bewerte, wie affin ein Unternehmen "
                    f"für das Software-Thema '{topic}' ist. Berücksichtige Projekte, "
                    "Partnerschaften, Produkte und Nachrichten zum Thema."
                ),
                prompt=(
                    f"Unternehmen: {company.name}\n"
                    f"Website: {company.website or 'unbekannt'}\n"
                    f"Branche: {company.industry or 'unbekannt'}\n"
                    f"Thema: {topic}\n\n"
                    f"Themenrelevante Nachrichten:\n{topic_text}\n\n"
                    "Bewerte die Affinität des Unternehmens für das Thema (0.0-1.0)."
                ),
                response_model=TopicAffinity,
            )

            combined = round(health.activity_score * 0.4 + affinity.affinity_score * 0.6, 3)

            relevance = TopicRelevance(
                company_health=health,
                topic_affinity=affinity,
                combined_score=combined,
            )

            return lead.model_copy(update={"topic_relevance": relevance})

    def _extract_leads(self, input_data: AgentResult | dict | None) -> list[Lead]:
        if isinstance(input_data, AgentResult):
            return input_data.leads

        if isinstance(input_data, dict):
            companies = input_data.get("companies", [])
            return [
                Lead(company=Company.model_validate(c) if isinstance(c, dict) else c)
                for c in companies
            ]

        return []
