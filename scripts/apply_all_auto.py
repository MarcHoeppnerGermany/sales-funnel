#!/usr/bin/env python3
"""Wendet alle data/auto_*.json Batchdateien an (apply_scores-Logik, --new).
Kompakte Ausgabe: pro Datei nur Anzahl neu/aktualisiert. Dedup-sicher
(Re-Run aktualisiert statt zu duplizieren).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.apply_scores import apply_entry, build_company, find_lead  # noqa: E402

ROOT = Path(__file__).parent.parent
LEADS_FILE = ROOT / "leads.json"


def main() -> None:
    data = json.loads(LEADS_FILE.read_text())
    files = sorted((ROOT / "data").glob("auto_*.json"))
    total_new = total_upd = 0
    problems = []

    for fp in files:
        try:
            batch = json.loads(fp.read_text())
        except Exception as exc:
            problems.append(f"{fp.name}: JSON kaputt ({exc})")
            continue
        pipeline, topic = batch["pipeline"], batch["topic"]
        n_new = n_upd = 0
        for entry in batch["leads"]:
            try:
                raw = find_lead(data["leads"], entry["name"])
                if raw is None:
                    scored = apply_entry(build_company(entry), entry, pipeline, topic)
                    data["leads"].append(scored.model_dump(mode="json"))
                    n_new += 1
                else:
                    scored = apply_entry(raw, entry, pipeline, topic)
                    data["leads"][data["leads"].index(raw)] = scored.model_dump(mode="json")
                    n_upd += 1
            except Exception as exc:
                problems.append(f"{fp.name} / {entry.get('name','?')}: {exc}")
        total_new += n_new
        total_upd += n_upd
        print(f"  {fp.name}: +{n_new} neu, {n_upd} aktualisiert")

    LEADS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGesamt: +{total_new} neu, {total_upd} aktualisiert, {len(data['leads'])} Leads total")
    if problems:
        print(f"\nPROBLEME ({len(problems)}):")
        for p in problems:
            print(f"  {p}")


if __name__ == "__main__":
    main()
