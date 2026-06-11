#!/usr/bin/env python3
"""Validierungs-Gate: prüft leads.json auf Vollständigkeit und Plausibilität.

Vor jedem Export ausführen. Exit-Code != 0 bei Fehlern.

Prüfungen:
- Schema-Validierung (Pydantic) für jeden Lead
- Platzhalter-Scores (0.25 = Default ohne Daten)
- Leads ohne topic_relevance / financials
- Namens-Duplikate
- Score-Konsistenz (gespeicherter vs. neu berechneter overall_score)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sales_funnel.models.schemas import Lead  # noqa: E402
from sales_funnel.scoring import score_overall  # noqa: E402

LEADS_FILE = Path(__file__).parent.parent / "leads.json"


def main() -> None:
    data = json.loads(LEADS_FILE.read_text())
    raw_leads = data["leads"]
    errors: list[str] = []
    warnings: list[str] = []

    # Schema-Validierung
    leads: list[Lead] = []
    for raw in raw_leads:
        try:
            leads.append(Lead.model_validate(raw))
        except Exception as exc:
            errors.append(f"Schema: {raw.get('company', {}).get('name', '?')}: {exc}")

    # Duplikate
    names = [lead.company.name for lead in leads]
    for name, count in Counter(names).items():
        if count > 1:
            errors.append(f"Duplikat ({count}x): {name}")

    # Vollständigkeit + Platzhalter
    incomplete = [l for l in leads if not l.topic_relevance or not l.financials]
    placeholder = [l for l in leads if l.overall_score == 0.25 and not l.financials]
    no_pipeline = [l for l in leads if not l.pipeline]

    if placeholder:
        errors.append(
            f"{len(placeholder)} Leads mit Platzhalter-Score 0.25 (ungescored): "
            + ", ".join(l.company.name for l in placeholder[:5])
            + ("..." if len(placeholder) > 5 else "")
        )
    if incomplete:
        warnings.append(
            f"{len(incomplete)} Leads ohne topic_relevance/financials: "
            + ", ".join(l.company.name for l in incomplete[:5])
            + ("..." if len(incomplete) > 5 else "")
        )
    if no_pipeline:
        warnings.append(f"{len(no_pipeline)} Leads ohne pipeline-Feld")

    # Score-Konsistenz
    drift = []
    for lead in leads:
        if lead.financials and lead.overall_score is not None:
            expected = score_overall(lead)
            if abs(expected - lead.overall_score) > 0.005:
                drift.append(f"{lead.company.name}: {lead.overall_score} != {expected}")
    if drift:
        warnings.append(f"{len(drift)} Leads mit Score-Drift: {drift[:3]}")

    # Report
    print(f"Leads gesamt:        {len(leads)}")
    print(f"Vollständig gescored: {len(leads) - len(incomplete)}")
    print(f"Mit Ansprechpartner:  {sum(1 for l in leads if l.contact_persons)}")
    print(f"Mit Pipeline-Feld:    {len(leads) - len(no_pipeline)}")
    print()
    for w in warnings:
        print(f"WARNUNG: {w}")
    for e in errors:
        print(f"FEHLER:  {e}")

    if errors:
        sys.exit(1)
    print("OK — keine blockierenden Fehler.")


if __name__ == "__main__":
    main()
