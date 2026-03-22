# Sales Lead Generator

Dieses Projekt nutzt Claude Code als AI-Engine für die Lead-Generierung.
Keine API-Keys nötig – Claude Code nutzt seine eigenen Tools (WebSearch, WebFetch).
Die Python-CLI (`sales-funnel`) verwaltet Daten, Scoring und Export.

## Installation

```bash
pip install -e .
```

## CLI-Befehle

```bash
# Lead hinzufügen
sales-funnel add --name "Firma" --website "firma.de" --industry "IT" --address "Berlin"
sales-funnel add --from-json firmen.json

# Leads verwalten
sales-funnel list [--format table|json] [--sort score|name]
sales-funnel show "Firmenname"
sales-funnel remove "Firmenname"

# Klassifizierung (Agent 2)
sales-funnel set-health "Firma" --score 0.8 --reasoning "..." --news "..."
sales-funnel set-affinity "Firma" --topic "Cloud" --score 0.9 --reasoning "..." --news "..."

# Firmenbewertung (Agent 3)
sales-funnel set-financials "Firma" --revenue "10M" --profit "2M" --employees 500
sales-funnel set-hiring "Firma" --score 0.7 --total-postings 50 --reasoning "..."
sales-funnel set-topic-hiring "Firma" --score 0.8 --relevant-postings 10 --reasoning "..." --positions "DevOps"
sales-funnel set-strategic "Firma" --size-fit 0.7 --financial-health 0.8 --pressure 0.6 --reasoning "..."

# Scoring & Export
sales-funnel score
sales-funnel export [--format json|csv|markdown] [--output datei]
sales-funnel import datei.json
```

## Workflow für Claude Code

### Agent 1: Adressgenerator
Wenn der User Firmen suchen will:
1. Nutze `WebSearch` um Firmen zu finden die zu den Kriterien passen (Branche, Themen, Region)
2. Für jede gefundene Firma:
   ```bash
   sales-funnel add --name "..." --website "..." --industry "..." --address "..."
   ```
3. Zeige die Liste: `sales-funnel list`

Beispiel-Suchen:
- `"Software Unternehmen Bayern Cloud Migration"`
- `"IT Dienstleister Berlin Kubernetes"`
- `"Automotive Softwareentwicklung Stuttgart"`

### Agent 2: Adressklassifizierer
Für jeden Lead in der Liste zwei Dimensionen bewerten:

**A) Firmengesundheit:**
1. `WebSearch` nach `"{Firmenname} Quartalsbericht news 2025 2026"`
2. Bewerte: Wie aktiv ist die Firma? Positive/negative Nachrichten?
3. ```bash
   sales-funnel set-health "Firma" --score 0.8 --reasoning "Positive Q3 Ergebnisse, Wachstum" --news "Umsatz gestiegen" --news "Neue Partnerschaft"
   ```

**B) Themen-Affinität:**
1. `WebSearch` nach `"{Firmenname} {Thema} Projekt Partnerschaft"`
2. Bewerte: Hat die Firma Bezug zum Thema?
3. ```bash
   sales-funnel set-affinity "Firma" --topic "Cloud Migration" --score 0.7 --reasoning "Mehrere Cloud-Projekte aktiv" --news "Migration auf AWS"
   ```

### Agent 3: Firmenklassifizierer
Für jeden Lead vier Dimensionen:

**Finanzdaten:**
1. `WebSearch` nach `"{Firma}" Umsatz Mitarbeiter`
2. ```bash
   sales-funnel set-financials "Firma" --revenue "50M EUR" --profit "5M EUR" --employees 300
   ```

**Generelle Hiring-Aktivität:**
1. `WebSearch` nach `"{Firma}" Stellenangebote jobs careers`
2. ```bash
   sales-funnel set-hiring "Firma" --score 0.7 --total-postings 45 --reasoning "Moderate Einstellungsaktivität"
   ```

**Themenbezogene Stellen:**
1. `WebSearch` nach `"{Firma}" jobs {Thema}`
2. ```bash
   sales-funnel set-topic-hiring "Firma" --score 0.9 --relevant-postings 8 --reasoning "Sucht aktiv Cloud-Experten" --positions "Cloud Architect" --positions "DevOps Engineer"
   ```

**Strategischer Fit:**
Basierend auf allen gesammelten Informationen:
- `size_fit`: Passt die Firmengröße als Kunde für uns?
- `financial_health`: Wie ist die finanzielle Lage?
- `pressure`: Hat die Firma Handlungsdruck im Thema? **WICHTIG: Auch schlecht situierte Firmen mit Druck sind sehr interessant!**
```bash
sales-funnel set-strategic "Firma" --size-fit 0.8 --financial-health 0.6 --pressure 0.9 --reasoning "Unter Modernisierungsdruck, muss dringend Cloud-Strategie umsetzen"
```

### Scoring & Abschluss
```bash
sales-funnel score           # Berechnet alle Gesamtscores
sales-funnel list --sort score  # Rangliste
sales-funnel export --format markdown  # Report
```

### Vollständige Pipeline
Alle drei Agenten nacheinander für alle Leads ausführen.
Am Ende: `sales-funnel export --format markdown`

## Scoring-Gewichtung

**Topic Relevance (Agent 2):**
- Firmengesundheit: 40%
- Themen-Affinität: 60%

**Overall Score:**
- Topic Relevance: 25%
- Strategic Fit: 30% (davon Pressure 50%, Size 25%, Financial Health 25%)
- Hiring: 15%
- Topic Hiring: 30%

**Customer Rating:**
- Hiring: 15%
- Topic Hiring: 35%
- Pressure: 30%
- Size Fit: 20%
