# Todo

## Datenqualitäts-Offensive (2026-05-28) — ABGESCHLOSSEN
- [x] 1. Schema erweitert: contact_persons, pipeline, tier, outreach im Lead-Modell
- [x] 2. Scoring 19 Energiehändler (Topic: Risikomanagement/ETRM)
- [x] 3. Scoring 25 Fernwärme (Topic: Betriebs- u. Anlagenverwaltung)
- [x] 4. Research-Agenten 24 Telematik (3 Batches à 8, read-only, JSON-Rückgabe)
- [x] 5. Scoring 24 Telematik via zentralen Applier
- [x] 6. Validierungs-Gate scripts/validate_leads.py (blockiert Exporte)
- [x] 7. Duplikate entfernt (Nordex SE Rostock, E-T-A ohne GmbH)
- [x] 8. Kontakte/Tiers/Outreach aus Markdown in leads.json migriert
- [x] 9. Generatoren (Excel/PDF) auf leads.json als Single Source umgestellt
- [x] 10. CLAUDE.md Agent-Regeln + lessons.md aktualisiert
- [x] 11. Exporte neu generiert, Gate grün (220 Leads, 100% gescort)

## Review
- 220 Leads, 0 Platzhalter, 84 mit Ansprechpartnern, 5 Pipelines
  (IoT 126, TISAX 24, Fernwärme 25, Energiehandel 19, Telematik 24)
- Wichtige Funde: Huber Automotive insolvent (Telematik), BEW Berlin mit
  gescheitertem 102-Mio-Leitwarten-Projekt (Top-Druck Fernwärme),
  Danpower/GETEC/BTB als HanseWerk-Natur-Zwillinge
- Offen (nächste Session): Telematik/Fernwärme/Energiehandel-Tiers vergeben,
  Outreach-Templates für deren Top-Leads, generate_word.py datengetrieben machen
