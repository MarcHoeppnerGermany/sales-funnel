from __future__ import annotations

import asyncio
from typing import Any

from pydantic import BaseModel

from sales_funnel.agents.base import BaseAgent
from sales_funnel.models.schemas import AgentResult, Company, Lead
from sales_funnel.services.llm import LLMService
from sales_funnel.services.search import SearchService


class CompanyList(BaseModel):
    companies: list[Company]


class AddressGenerator(BaseAgent):
    """Agent 1: Findet potenzielle Interessenten anhand von Suchkriterien."""

    name = "address_generator"

    def __init__(
        self,
        llm: LLMService | None = None,
        search: SearchService | None = None,
    ):
        self.llm = llm or LLMService()
        self.search = search or SearchService()

    async def run(self, input_data: AgentResult | dict | None = None) -> AgentResult:
        if isinstance(input_data, AgentResult):
            criteria = input_data.metadata.get("criteria", {})
        elif isinstance(input_data, dict):
            criteria = input_data
        else:
            criteria = {}

        industry = criteria.get("industry", "Software")
        topics = criteria.get("topics", [])
        location = criteria.get("location", "Deutschland")
        max_results = criteria.get("max_results", 20)

        # Suchbegriffe generieren
        queries = await self.llm.generate_search_queries(
            {
                "industry": industry,
                "topics": topics,
                "location": location,
                "goal": "Unternehmen finden die als Kunden für Softwareentwicklung in Frage kommen",
            }
        )

        # Web-Suche durchführen
        all_results = []
        search_tasks = [self.search.search(q, num_results=10) for q in queries]
        for batch in await asyncio.gather(*search_tasks, return_exceptions=True):
            if isinstance(batch, list):
                all_results.extend(batch)

        if not all_results:
            return AgentResult(
                agent_name=self.name,
                leads=[],
                metadata={"criteria": criteria, "queries": queries, "note": "Keine Suchergebnisse"},
            )

        # Suchergebnisse durch Claude analysieren lassen
        search_text = "\n".join(
            f"- {r.title} | {r.url} | {r.snippet}" for r in all_results
        )

        company_list = await self.llm.structured_query(
            system=(
                "Du bist ein B2B-Recherche-Experte. Extrahiere Unternehmen aus den "
                "Suchergebnissen. Dedupliziere nach Domain. Gib nur echte Unternehmen "
                "zurück, keine Nachrichtenportale oder Verzeichnisse."
            ),
            prompt=(
                f"Extrahiere bis zu {max_results} Unternehmen aus diesen Suchergebnissen.\n"
                f"Branche: {industry}\n"
                f"Themen: {', '.join(topics) if topics else 'allgemein'}\n"
                f"Region: {location}\n\n"
                f"Suchergebnisse:\n{search_text}"
            ),
            response_model=CompanyList,
        )

        leads = [Lead(company=c) for c in company_list.companies[:max_results]]

        return AgentResult(
            agent_name=self.name,
            leads=leads,
            metadata={
                "criteria": criteria,
                "queries": queries,
                "search_results_count": len(all_results),
                "tokens": {
                    "input": self.llm.total_input_tokens,
                    "output": self.llm.total_output_tokens,
                },
            },
        )
