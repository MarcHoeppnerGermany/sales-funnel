#!/usr/bin/env python3
"""Vergibt tier für ALLE Leads anhand overall_score (autoritativ), mit
Ausnahme einer Pin-Liste hand-kuratierter IoT-Leads (strategische TIER1/2
trotz niedrigerem Score, z.B. SH Netz/HanseWerk-Bezug).

Schwellen:
  TIER1 >= 0.68   heiß  (Direktansprache priorisiert)
  TIER2 0.56-0.68 warm
  TIER3 <  0.56   kalt
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LEADS_FILE = Path(__file__).parent.parent / "leads.json"

# Hand-kuratierte IoT-Leads, die unabhängig vom Score TIER1 bleiben
PINNED_TIER1 = {
    "SH Netz AG (HanseWerk)", "Harburg-Freudenberger Maschinenbau (HF Group)",
    "Klosterfrau Healthcare Group", "Nordex SE", "Sikora AG",
    "Stern-Wywiol Gruppe", "GP JOULE GmbH", "ACO Severin Ahlmann",
    "Fritz Winter Eisengießerei",
}


def tier_for(score: float) -> str:
    if score >= 0.68:
        return "TIER1"
    if score >= 0.56:
        return "TIER2"
    return "TIER3"


def main() -> None:
    data = json.loads(LEADS_FILE.read_text())
    for lead in data["leads"]:
        name = lead["company"]["name"]
        if name in PINNED_TIER1:
            lead["tier"] = "TIER1"
        else:
            lead["tier"] = tier_for(lead.get("overall_score") or 0)
    LEADS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    by = Counter(l.get("tier") for l in data["leads"])
    print("Tier-Verteilung: " + " | ".join(f"{t}:{by[t]}" for t in ("TIER1", "TIER2", "TIER3")))


if __name__ == "__main__":
    main()
