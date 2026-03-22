from __future__ import annotations

import json
from pathlib import Path

from sales_funnel.models.schemas import AgentResult, Lead


class LeadStore:
    """Persistiert Leads in einer JSON-Datei."""

    def __init__(self, path: str = "leads.json"):
        self.path = Path(path)

    def load(self) -> AgentResult:
        """Lädt Leads aus Datei."""
        if not self.path.exists():
            return AgentResult(agent_name="store", leads=[], metadata={})
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return AgentResult.model_validate(data)

    def save(self, result: AgentResult) -> None:
        """Speichert Leads in Datei."""
        self.path.write_text(
            result.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def add_leads(self, leads: list[Lead]) -> AgentResult:
        """Fügt Leads hinzu (dedupliziert nach Firmenname)."""
        result = self.load()
        existing = {lead.company.name.lower() for lead in result.leads}
        for lead in leads:
            key = lead.company.name.lower()
            if key not in existing:
                result.leads.append(lead)
                existing.add(key)
        self.save(result)
        return result

    def update_lead(self, company_name: str, **kwargs) -> Lead:
        """Aktualisiert einen Lead."""
        result = self.load()
        for i, lead in enumerate(result.leads):
            if lead.company.name.lower() == company_name.lower():
                result.leads[i] = lead.model_copy(update=kwargs)
                self.save(result)
                return result.leads[i]
        raise KeyError(f"Lead nicht gefunden: {company_name}")

    def get_lead(self, company_name: str) -> Lead | None:
        """Einzelnen Lead holen."""
        result = self.load()
        for lead in result.leads:
            if lead.company.name.lower() == company_name.lower():
                return lead
        return None

    def remove_lead(self, company_name: str) -> bool:
        """Lead entfernen."""
        result = self.load()
        original_len = len(result.leads)
        result.leads = [
            lead
            for lead in result.leads
            if lead.company.name.lower() != company_name.lower()
        ]
        if len(result.leads) < original_len:
            self.save(result)
            return True
        return False
