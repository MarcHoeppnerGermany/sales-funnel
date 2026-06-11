#!/usr/bin/env python3
"""Zentraler Applier: schreibt Scoring-Batchdaten validiert in leads.json.

Nutzung: python3 scripts/apply_scores.py data/scoring_<pipeline>.json

Batchdatei-Format:
{
  "pipeline": "Energiehandel",
  "topic": "Risikomanagement / ETRM",
  "leads": [ { "name": ..., "health_score": ..., ... } ]
}

Einziger Schreibpfad für Scoring-Daten — Agenten liefern nur JSON,
persistiert wird ausschließlich hier (Schema-validiert via Pydantic).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sales_funnel.models.schemas import (  # noqa: E402
    CompanyFinancials,
    CompanyHealth,
    ContactPerson,
    HiringActivity,
    Lead,
    StrategicFit,
    TopicAffinity,
    TopicHiring,
)
from sales_funnel.scoring import (  # noqa: E402
    score_customer_rating,
    score_overall,
    score_topic_relevance,
)

LEADS_FILE = Path(__file__).parent.parent / "leads.json"


def find_lead(leads: list[dict], name: str) -> dict | None:
    # Exakter Match hat Vorrang — Fuzzy nur als Fallback (Lesson: E-T-A-Duplikat)
    for lead in leads:
        if lead["company"]["name"] == name:
            return lead
    matches = [
        lead for lead in leads
        if name in lead["company"]["name"] or lead["company"]["name"] in name
    ]
    if len(matches) > 1:
        raise ValueError(f"Mehrdeutiger Name '{name}': {[m['company']['name'] for m in matches]}")
    return matches[0] if matches else None


def build_company(entry: dict) -> dict:
    """Stammdaten für einen NEUEN Lead aus dem Batch-Entry."""
    return {
        "company": {
            "name": entry["name"],
            "website": entry.get("website"),
            "address": entry.get("address"),
            "industry": entry.get("industry"),
            "source": entry.get("source"),
        }
    }


def apply_entry(raw_lead: dict, entry: dict, pipeline: str, topic: str) -> Lead:
    """Baut ein vollständig gescortes Lead-Objekt aus Batch-Daten."""
    lead = Lead.model_validate(raw_lead)
    lead.pipeline = pipeline
    # Stammdaten ergänzen, falls im Batch mitgeliefert (neue Leads / Updates)
    if entry.get("website"):
        lead.company.website = entry["website"]
    if entry.get("address"):
        lead.company.address = entry["address"]
    if entry.get("industry"):
        lead.company.industry = entry["industry"]

    health = CompanyHealth(
        activity_score=entry["health_score"],
        activity_reasoning=entry["health_reasoning"],
        recent_news=entry.get("recent_news", []),
    )
    affinity = TopicAffinity(
        topic=topic,
        affinity_score=entry["affinity_score"],
        affinity_reasoning=entry["affinity_reasoning"],
        relevant_news=entry.get("relevant_news", []),
    )
    lead.topic_relevance = score_topic_relevance(health, affinity)

    strategic = StrategicFit(
        size_fit_score=entry["size_fit"],
        financial_health_score=entry["financial_health"],
        pressure_score=entry["pressure"],
        strategic_reasoning=entry["strategic_reasoning"],
    )
    rating = score_customer_rating(
        hiring_score=entry["hiring_score"],
        topic_hiring_score=entry["topic_hiring_score"],
        pressure_score=entry["pressure"],
        size_fit_score=entry["size_fit"],
    )
    lead.financials = CompanyFinancials(
        revenue_estimate=entry.get("revenue"),
        profit_estimate=entry.get("profit"),
        employee_count=entry.get("employees") or None,
        hiring_activity=HiringActivity(
            general_hiring_score=entry["hiring_score"],
            total_job_postings=entry.get("hiring_postings"),
            hiring_reasoning=entry["hiring_reasoning"],
        ),
        topic_hiring=TopicHiring(
            topic_hiring_score=entry["topic_hiring_score"],
            relevant_job_postings=entry.get("topic_postings"),
            topic_hiring_reasoning=entry["topic_hiring_reasoning"],
            example_positions=entry.get("example_positions", []),
        ),
        strategic_fit=strategic,
        customer_rating=rating,
        rating_reasoning=entry["strategic_reasoning"],
    )

    # Kontakte ohne Namen verwerfen (Agenten liefern teils name:null)
    lead.contact_persons = [
        ContactPerson.model_validate(c)
        for c in entry.get("contacts", [])
        if isinstance(c, dict) and c.get("name")
    ]
    lead.overall_score = score_overall(lead)
    return lead


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Nutzung: apply_scores.py <batchdatei.json>")

    batch = json.loads(Path(sys.argv[1]).read_text())
    pipeline, topic = batch["pipeline"], batch["topic"]

    allow_new = "--new" in sys.argv or batch.get("allow_new", False)
    data = json.loads(LEADS_FILE.read_text())
    updated, created = [], []

    for entry in batch["leads"]:
        raw = find_lead(data["leads"], entry["name"])
        if raw is None:
            if not allow_new:
                sys.exit(f"NICHT GEFUNDEN (kein --new): {entry['name']}")
            raw = build_company(entry)
            scored = apply_entry(raw, entry, pipeline, topic)
            data["leads"].append(scored.model_dump(mode="json"))
            created.append((entry["name"], scored.overall_score))
        else:
            scored = apply_entry(raw, entry, pipeline, topic)
            data["leads"][data["leads"].index(raw)] = scored.model_dump(mode="json")
            updated.append((entry["name"], scored.overall_score))

    LEADS_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Pipeline: {pipeline} | Topic: {topic}")
    print(f"Neu: {len(created)} | Aktualisiert: {len(updated)}")
    for name, score in sorted(created + updated, key=lambda x: -x[1]):
        print(f"  {score:.3f}  {name}")


if __name__ == "__main__":
    main()
