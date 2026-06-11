#!/usr/bin/env python3
"""Erzeugt leads_uebersicht.md: kompakte Übersicht aller Pipelines mit
Tier-Verteilung und Top-15-Leads je Pipeline. Liest nur leads.json."""
import json
from collections import Counter
from datetime import date
from pathlib import Path

LEADS = Path(__file__).parent.parent / "leads.json"
OUT = Path(__file__).parent.parent / "leads_uebersicht.md"

PIPE_TOPIC = {
    "Energie": "Betriebs- & Anlagenverwaltung / ETRM",
    "IoT": "IoT-Plattform-Entwicklung",
    "Telematik": "Embedded-/Telematik-Softwareentwicklung",
    "TISAX": "TISAX-konformes IT-Outsourcing (Cloud/IoT/AI)",
}


def main():
    leads = json.loads(LEADS.read_text())["leads"]
    lines = [
        "# Lead-Übersicht — alle Pipelines",
        "",
        f"Stand: {date.today().isoformat()} · {len(leads)} Leads gesamt",
        "",
        "Quelle: `leads.json` (Single Source of Truth). Vollständige Daten in "
        "`iot_leads_komplett.xlsx`, Lead-Sheets in `iot_lead_sheets.pdf`, "
        "Anschreiben in `iot_outreach_vorlagen.docx`.",
        "",
        "## Pipelines",
        "",
        "| Pipeline | Thema | Leads | TIER1 | TIER2 | TIER3 |",
        "|---|---|--:|--:|--:|--:|",
    ]
    pipes = ["Energie", "IoT", "Telematik", "TISAX"]
    for p in pipes:
        sub = [l for l in leads if l.get("pipeline") == p]
        t = Counter(l.get("tier") for l in sub)
        lines.append(f"| {p} | {PIPE_TOPIC.get(p,'')} | {len(sub)} | "
                     f"{t['TIER1']} | {t['TIER2']} | {t['TIER3']} |")
    lines += ["", "---", ""]

    for p in pipes:
        sub = sorted([l for l in leads if l.get("pipeline") == p],
                     key=lambda x: -(x.get("overall_score") or 0))
        lines += [f"## {p} — Top 15", "",
                  "| # | Score | Tier | Firma | Standort | Ansprechpartner |",
                  "|--:|--:|---|---|---|---|"]
        for i, l in enumerate(sub[:15], 1):
            cps = l.get("contact_persons") or []
            contact = cps[0]["name"] + (f" ({cps[0].get('role','')})" if cps[0].get("role") else "") if cps else "—"
            lines.append(f"| {i} | {l.get('overall_score',0):.0%} | {l.get('tier','')} | "
                         f"{l['company']['name']} | {l['company'].get('address','')} | {contact} |")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Übersicht erstellt: {OUT.name} ({len(leads)} Leads)")


if __name__ == "__main__":
    main()
