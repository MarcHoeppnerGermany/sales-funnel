# Todo — Pipeline-Ausbau (2026-05-28)

## Ziel
- Energie (= Fernwärme + Energieversorger + Energiehandel zusammengelegt): 100 Leads
  → eigene Rubrik "Energiehandel" entfällt, geht in "Energie" auf
- IoT: aktualisieren + auf 150 Leads
- Telematik: auf 100 Leads
- TISAX: auf 100 Leads
- Alle Outreach-Texte/Unterlagen für Direktansprache fertig

## Schritte
- [ ] 1. apply_scores.py: NEUE Leads anlegen können (Company-Block + idempotent)
- [ ] 2. Pipelines umbenennen: Energiehandel+Fernwaerme -> "Energie"
- [ ] 3. Research-Agenten Energie (Ziel +56) — Segmente, je <=8, eigene Batchdatei
- [ ] 4. Research-Agenten Telematik (Ziel +76)
- [ ] 5. Research-Agenten TISAX (Ziel +76)
- [ ] 6. Research-Agenten IoT (Ziel +24)
- [ ] 7. Alle Batches via apply_scores.py einspielen, dedupen
- [ ] 8. Validierungs-Gate grün
- [ ] 9. Tiers über alle Pipelines vergeben (scoreschwellen-basiert)
- [ ] 10. Outreach (subject+hook) für alle TIER1/TIER2 generieren
- [ ] 11. generate_word.py datengetrieben; Excel/PDF/Word neu bauen
- [ ] 12. Commit + Push

## Bestand vor Ausbau
- IoT 126, TISAX 24, Fernwaerme 25, Telematik 24, Energiehandel 19 = 218 (+2 = 220)
