# Lessons Learned

## 2026-03-22: Initiales Setup
- **Keine externen API-Keys voraussetzen**: Wenn das Tool innerhalb von Claude Code läuft, sind WebSearch/WebFetch bereits verfügbar. Kein Anthropic SDK oder Brave API nötig.
- **Linter-Änderungen sofort committen**: Wenn der Linter Dateien ändert, diese nicht ignorieren sondern direkt mit-committen.

## 2026-05-28: Datenqualitäts-Offensive (Review-Erkenntnisse)

- **Agent-Batchgröße max. 8 Firmen**: Ein 19-Firmen-Scoring-Agent starb nach
  30 Min Timeout — die Arbeit war komplett verloren und fiel wochenlang nicht
  auf. Drei 8er-Batches liefen dagegen in je ~4 Min sauber durch.
- **"Mache ich selbst" ohne Todo = vergessen**: Nach dem Agent-Timeout wurde
  die Nacharbeit angekündigt, aber nie ausgeführt — 68 Leads (31%) hatten
  monatelang Platzhalter-Scores (0.25) und landeten so im Excel-Export.
  Regel: Jede angekündigte Nacharbeit SOFORT in tasks/todo.md eintragen.
- **Platzhalter-Scores sind unsichtbar giftig**: score_overall() liefert 0.25
  bei fehlenden Daten — sieht aus wie ein echter (schlechter) Score.
  Gegenmittel: scripts/validate_leads.py blockiert Exporte bei 0.25-Leads.
- **Agenten dürfen nicht selbst persistieren**: Zwei Agenten schrieben direkt
  in leads.json (Konfliktrisiko, kein Schema-Zwang), andere lieferten nur Text.
  Jetzt einheitlich: Agenten liefern JSON, scripts/apply_scores.py schreibt.
- **Fuzzy-Name-Matching braucht Exact-First**: "E-T-A Elektrotechnische
  Apparate" existierte mit und ohne "GmbH" — der Substring-Match traf das
  falsche Objekt. apply_scores.py prüft jetzt exakt vor fuzzy und wirft bei
  Mehrdeutigkeit einen Fehler.
- **Daten gehören ins Datenmodell, nicht in Skripte**: Kontakte/Tiers/Outreach
  waren 3x in Generator-Skripten hardcodet. Jetzt: Lead-Schema um
  contact_persons/pipeline/tier/outreach erweitert, Generatoren lesen nur
  noch leads.json.
- **Write-Calls unter ~250 Zeilen halten**: Große Einzel-Writes provozieren
  Stream-Timeouts; lieber Datei in 2-3 Schritten aufbauen (Write + Edit).
- **pip-Umgebung ist flüchtig**: fpdf2 braucht nach jedem Umgebungs-Reset
  `pip install --force-reinstall cffi` (pyo3/cryptography-Konflikt).

## 2026-05-28: Pipeline-Ausbau auf 455 Leads (30+ Agenten)

- **Agenten schreiben eigene Batchdateien**: Bei großem Volumen (~230 neue
  Firmen) Daten NICHT durch den Hauptkontext schleusen. Agenten schreiben je
  eine data/auto_<pipeline>_<n>.json (apply_scores-Format) und antworten nur
  mit einer Zeile. Spart massiv Kontext, skaliert auf 30 parallele Agenten.
- **Read-only-Regel präzisiert**: Agenten dürfen eigene Batchdateien schreiben
  (getrennte Files, kein Konflikt), aber NIE leads.json. Persistierung zentral
  über apply_all_auto.py → apply_scores (Pydantic-validiert).
- **name:null bei Kontakten abfangen**: Agenten liefern bei fehlendem Kontakt
  oft {"name": null} — ContactPerson.name ist Pflicht-str. apply_entry filtert
  Kontakte ohne Namen jetzt heraus, statt am ganzen Batch zu scheitern.
- **Normalisierte Dedup nach Massen-Import**: Exakt-Dedup reicht nicht (z.B.
  "COUPLINK Group AG" vs "Couplink Group AG"). Nach jedem Import normalisierten
  Dup-Check fahren (lowercase + Rechtsform/Klammern strippen).
- **Segment-Vorgabe verhindert Agent-Überlappung**: Jedem Research-Agenten ein
  klar abgegrenztes Marktsegment + Beispiel-Firmen + Ausschlussliste geben.
  Überlappung blieb minimal (nur 4 Cross-Updates bei 232 Firmen).
- **Tier-Schwellen autoritativ + Pin-Liste**: Score-basierte Tiers über alle
  Pipelines, aber hand-kuratierte strategische TIER1 (HanseWerk-Bezug etc.)
  per Pin-Liste schützen, sonst werden sie vom Score überstimmt.
