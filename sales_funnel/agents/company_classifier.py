from __future__ import annotations

import asyncio

from pydantic import BaseModel

from sales_funnel.agents.base import BaseAgent
from sales_funnel.models.schemas import (
    AgentResult,
    CompanyFinancials,
    HiringActivity,
    Lead,
    StrategicFit,
    TopicHiring,
)
from sales_funnel.services.llm import LLMService
from sales_funnel.services.search import SearchService


class FinancialData(BaseModel):
    """Hilfsmodell für die LLM-Antwort zu Finanzdaten."""

    revenue_estimate: str | None = None
    profit_estimate: str | None = None
    employee_count: int | None = None


class CompanyClassifier(BaseAgent):
    """Agent 3: Bewertet Unternehmen als potenzielle Kunden.

    Analysiert:
    - Finanzkennzahlen (Umsatz, Gewinn, Mitarbeiter)
    - Generelle Einstellungsaktivität (Wachstumsindikator)
    - Themenbezogene Stellenanzeigen (Investition ins Thema)
    - Strategischer Fit (Größe, Finanzlage, Handlungsdruck)

    Wichtig: Auch Firmen denen es nicht gut geht, die aber dadurch Druck
    im Thema haben, werden als interessant bewertet.
    """

    name = "company_classifier"

    def __init__(
        self,
        context: str = "",
        llm: LLMService | None = None,
        search: SearchService | None = None,
        max_concurrent: int = 5,
    ):
        self.context = context
        self.llm = llm or LLMService()
        self.search = search or SearchService()
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def run(self, input_data: AgentResult | dict | None = None) -> AgentResult:
        if not isinstance(input_data, AgentResult):
            raise ValueError("CompanyClassifier benötigt AgentResult als Input")

        context = self.context or input_data.metadata.get("topic", "Softwareentwicklung")

        tasks = [self._classify_company(lead, context) for lead in input_data.leads]
        classified = await asyncio.gather(*tasks, return_exceptions=True)

        result_leads = []
        for item in classified:
            if isinstance(item, Lead):
                result_leads.append(item)

        # Gesamtscore berechnen
        for lead in result_leads:
            topic_score = (
                lead.topic_relevance.combined_score if lead.topic_relevance else 0.5
            )
            fin = lead.financials
            if fin:
                hiring_score = fin.hiring_activity.general_hiring_score if fin.hiring_activity else 0.0
                topic_hiring_score = fin.topic_hiring.topic_hiring_score if fin.topic_hiring else 0.0
                strategic = fin.strategic_fit

                if strategic:
                    # Strategischer Fit: Kombination aus Größe, Finanzgesundheit und Druck
                    # Druck-Score wird besonders gewichtet – auch schlecht situierte Firmen
                    # mit hohem Handlungsdruck sind sehr interessante Kunden
                    strategic_score = (
                        strategic.size_fit_score * 0.25
                        + strategic.financial_health_score * 0.25
                        + strategic.pressure_score * 0.50
                    )
                else:
                    strategic_score = 0.5

                # Gewichtung: Themenrelevanz 25%, Strategic Fit 30%, Hiring 15%, Topic-Hiring 30%
                lead.overall_score = round(
                    topic_score * 0.25
                    + strategic_score * 0.30
                    + hiring_score * 0.15
                    + topic_hiring_score * 0.30,
                    3,
                )
            else:
                lead.overall_score = round(topic_score * 0.5, 3)

        result_leads.sort(key=lambda l: l.overall_score or 0, reverse=True)

        return AgentResult(
            agent_name=self.name,
            leads=result_leads,
            metadata={
                "context": context,
                "classified_count": len(result_leads),
                "tokens": {
                    "input": self.llm.total_input_tokens,
                    "output": self.llm.total_output_tokens,
                },
            },
        )

    async def _classify_company(self, lead: Lead, context: str) -> Lead:
        async with self._semaphore:
            company = lead.company

            # Drei parallele Suchen
            finance_query = f'"{company.name}" Umsatz OR revenue OR Mitarbeiter OR employees'
            hiring_query = f'"{company.name}" Stellenangebote OR jobs OR careers'
            topic_hiring_query = f'"{company.name}" Stellenanzeige OR job {context}'

            finance_results, hiring_results, topic_hiring_results = await asyncio.gather(
                self.search.search(finance_query, num_results=5),
                self.search.search(hiring_query, num_results=5),
                self.search.search(topic_hiring_query, num_results=5),
            )

            # Finanzdaten extrahieren
            finance_text = "\n".join(
                f"- {r.title}: {r.snippet}" for r in finance_results
            ) or "Keine Finanzdaten gefunden."

            fin_data = await self.llm.structured_query(
                system=(
                    "Du bist ein Business-Intelligence-Analyst. "
                    "Schätze Finanzkennzahlen basierend auf verfügbaren Informationen."
                ),
                prompt=(
                    f"Unternehmen: {company.name}\n"
                    f"Branche: {company.industry or 'unbekannt'}\n\n"
                    f"Recherche:\n{finance_text}\n\n"
                    "Schätze Umsatz, Gewinn und Mitarbeiteranzahl."
                ),
                response_model=FinancialData,
            )

            # Dimension A: Generelle Einstellungsaktivität
            hiring_text = "\n".join(
                f"- {r.title}: {r.snippet}" for r in hiring_results
            ) or "Keine Stellenanzeigen gefunden."

            hiring = await self.llm.structured_query(
                system=(
                    "Du bist ein HR-Analyst. Bewerte, wie aktiv ein Unternehmen "
                    "generell Mitarbeiter sucht. Viele offene Stellen sind ein gutes Zeichen "
                    "für Wachstum und Budget."
                ),
                prompt=(
                    f"Unternehmen: {company.name}\n\n"
                    f"Stellenanzeigen-Recherche:\n{hiring_text}\n\n"
                    "Bewerte die generelle Einstellungsaktivität (0.0-1.0)."
                ),
                response_model=HiringActivity,
            )

            # Dimension B: Themenbezogene Stellen
            topic_hiring_text = "\n".join(
                f"- {r.title}: {r.snippet}" for r in topic_hiring_results
            ) or "Keine themenrelevanten Stellenanzeigen gefunden."

            topic_hiring = await self.llm.structured_query(
                system=(
                    f"Du bist ein HR-Analyst. Bewerte, ob das Unternehmen Personal sucht, "
                    f"das zum Thema '{context}' passt. Relevante Stellenanzeigen deuten "
                    f"darauf hin, dass die Firma in diesem Bereich investiert."
                ),
                prompt=(
                    f"Unternehmen: {company.name}\n"
                    f"Thema: {context}\n\n"
                    f"Themenrelevante Stellenanzeigen:\n{topic_hiring_text}\n\n"
                    "Bewerte, ob die Firma themenbezogenes Personal sucht (0.0-1.0). "
                    "Liste Beispiel-Positionen auf."
                ),
                response_model=TopicHiring,
            )

            # Strategische Bewertung: Sammle alle bisherigen Infos
            health_info = ""
            if lead.topic_relevance and lead.topic_relevance.company_health:
                h = lead.topic_relevance.company_health
                health_info = (
                    f"Firmengesundheit (aus Nachrichtenanalyse): {h.activity_score}/1.0\n"
                    f"Begründung: {h.activity_reasoning}\n"
                )

            strategic_fit = await self.llm.structured_query(
                system=(
                    "Du bist ein strategischer B2B-Vertriebsberater. Bewerte, ob eine Firma "
                    "als Kunde für uns passt. Berücksichtige dabei:\n"
                    "- Größenordnung: Passt die Firma zu einem mittelständischen IT-Dienstleister?\n"
                    "- Finanzielle Lage: Gut situiert = kann investieren.\n"
                    "- WICHTIG: Auch Firmen denen es NICHT gut geht, können sehr interessante "
                    "Kunden sein, wenn sie dadurch Handlungsdruck im Thema haben! "
                    "Eine Firma unter Druck, die z.B. dringend modernisieren muss, "
                    "ist oft ein besserer Lead als eine zufriedene, gut situierte Firma."
                ),
                prompt=(
                    f"Unternehmen: {company.name}\n"
                    f"Branche: {company.industry or 'unbekannt'}\n"
                    f"Thema: {context}\n\n"
                    f"Finanzdaten: Umsatz {fin_data.revenue_estimate or 'unbekannt'}, "
                    f"Gewinn {fin_data.profit_estimate or 'unbekannt'}, "
                    f"{fin_data.employee_count or '?'} Mitarbeiter\n\n"
                    f"Einstellungsaktivität: {hiring.general_hiring_score}/1.0 – {hiring.hiring_reasoning}\n"
                    f"Themenbez. Stellen: {topic_hiring.topic_hiring_score}/1.0 – {topic_hiring.topic_hiring_reasoning}\n\n"
                    f"{health_info}\n"
                    "Bewerte den strategischen Fit als potenziellen Kunden."
                ),
                response_model=StrategicFit,
            )

            # Kunden-Rating: Kombination aus Hiring und strategischem Fit
            customer_rating = round(
                hiring.general_hiring_score * 0.15
                + topic_hiring.topic_hiring_score * 0.35
                + strategic_fit.pressure_score * 0.30
                + strategic_fit.size_fit_score * 0.20,
                3,
            )

            financials = CompanyFinancials(
                revenue_estimate=fin_data.revenue_estimate,
                profit_estimate=fin_data.profit_estimate,
                employee_count=fin_data.employee_count,
                hiring_activity=hiring,
                topic_hiring=topic_hiring,
                strategic_fit=strategic_fit,
                customer_rating=customer_rating,
                rating_reasoning=(
                    f"Strategic: {strategic_fit.strategic_reasoning} | "
                    f"Hiring: {hiring.hiring_reasoning} | "
                    f"Topic-Hiring: {topic_hiring.topic_hiring_reasoning}"
                ),
            )

            return lead.model_copy(update={"financials": financials})
