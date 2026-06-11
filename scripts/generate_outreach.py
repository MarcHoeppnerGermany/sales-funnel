#!/usr/bin/env python3
"""Erzeugt outreach (subject + hook) für TIER1/TIER2-Leads OHNE bestehende
Vorlage. Grundlage: pipeline-spezifische Value Proposition + die konkrete
affinity_reasoning des jeweiligen Leads (= echte Personalisierung).

Hand-kuratierte Outreach-Einträge (IoT TIER1) bleiben erhalten.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

LEADS_FILE = Path(__file__).parent.parent / "leads.json"

# Value Proposition + Betreff-Muster je Pipeline (und Topic-Sonderfall ETRM)
SUBJECTS = {
    "IoT": "{name}: IoT-Plattform & Anlagen-Monitoring aus einer Hand?",
    "Energie": "{name}: Betriebs- & Anlagenverwaltung — 24 Jahre Erfahrung mit HanseWerk Natur",
    "Energie_ETRM": "{name}: Risikomanagement-/ETRM-System für Ihren Energiehandel?",
    "Telematik": "{name}: Embedded-/Telematik-Entwicklung als verlängerte Werkbank?",
    "TISAX": "{name}: TISAX-konformes IT-Outsourcing (Cloud/IoT/AI)?",
}

INTRO = {
    "IoT": ("Wir bauen seit über 20 Jahren IoT- und Anlagenverwaltungs-Plattformen "
            "(24 Jahre Betriebsführung für den Energieversorger HanseWerk Natur)."),
    "Energie": ("Wir haben 24 Jahre die komplette Betriebs- und Anlagenverwaltung für "
                "HanseWerk Natur entwickelt und betrieben — Architektur, Entwicklung, Testing, Betrieb."),
    "Energie_ETRM": ("Wir entwickeln Software für Energiehandel und Risikomanagement und "
                     "kennen die Anforderungen physischer Händler aus 24 Jahren Energiebranche."),
    "Telematik": ("Wir entwickeln seit über 20 Jahren Embedded- und Telematik-Software — "
                  "von der Steuergeräte-Nähe bis zur Cloud-Plattform."),
    "TISAX": ("Wir sind Ihr TISAX-konformer IT-Entwicklungs- und Cloud-Partner für "
              "Automotive-Zulieferer (IoT, KI, Datenplattformen)."),
}

CTA = "Hätten Sie 20 Minuten für einen kurzen Austausch — gerne mit einem 2-Minuten-Video vorab?"


def short_name(name: str) -> str:
    s = name
    for suf in [" GmbH & Co. KG", " GmbH & Co KG", " GmbH", " AG", " SE", " KG",
                " KGaA", " mbH", " e.G.", " eG"]:
        s = s.replace(suf, "")
    s = re.sub(r"\s*\(.*?\)\s*", "", s).strip()
    return s or name


def first_sentence(text: str, maxlen: int = 220) -> str:
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?;])\s+", text.strip())
    out = parts[0] if parts else text
    return out[:maxlen].rstrip(" .,;") + "." if out else ""


def variant(lead: dict) -> str:
    pipeline = lead.get("pipeline")
    topic = ((lead.get("topic_relevance") or {}).get("topic_affinity") or {}).get("topic", "")
    if pipeline == "Energie" and "ETRM" in topic:
        return "Energie_ETRM"
    return pipeline


def main() -> None:
    data = json.loads(LEADS_FILE.read_text())
    n = 0
    for lead in data["leads"]:
        if lead.get("tier") not in ("TIER1", "TIER2"):
            continue
        if lead.get("outreach") and (lead["outreach"].get("subject")):
            continue  # hand-kuratiert / schon vorhanden
        v = variant(lead)
        if v not in SUBJECTS:
            continue
        name = short_name(lead["company"]["name"])
        affinity = ((lead.get("topic_relevance") or {}).get("topic_affinity") or {})
        hook = first_sentence(affinity.get("affinity_reasoning", ""))
        lead["outreach"] = {
            "subject": SUBJECTS[v].format(name=name),
            "hook": hook,
        }
        n += 1
    LEADS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Outreach (subject+hook) generiert: {n}")


if __name__ == "__main__":
    main()
