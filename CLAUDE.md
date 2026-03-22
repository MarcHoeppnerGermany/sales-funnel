# Sales Lead Generator

Dieses Projekt nutzt Claude Code als AI-Engine für die Lead-Generierung.
Die Python-CLI (`sales-funnel`) verwaltet Daten, Scoring und Export.

## Architektur

- `sales_funnel/models/schemas.py` - Pydantic-Datenmodelle (Company, Lead, Scores etc.)
- `sales_funnel/store.py` - JSON-basierte Lead-Persistierung
- `sales_funnel/scoring.py` - Scoring-Logik (rein Python, keine API-Aufrufe)
- `sales_funnel/cli.py` - CLI mit argparse-Subcommands

## CLI-Befehle

```bash
# Leads verwalten
sales-funnel add --name "SAP SE" --website "sap.com" --industry "Enterprise Software" --address "Walldorf"
sales-funnel add --from-json companies.json
sales-funnel list [--format table|json] [--sort score|name]
sales-funnel show "SAP SE"
sales-funnel remove "SAP SE"

# Klassifizierung setzen
sales-funnel set-health "SAP SE" --score 0.8 --reasoning "Aktiv, Q3 positiv" --news "SAP Q3 Rekordumsatz"
sales-funnel set-affinity "SAP SE" --topic "Cloud Migration" --score 0.9 --reasoning "Stark in Cloud" --news "SAP BTP Expansion"

# Firmenbewertung setzen
sales-funnel set-financials "SAP SE" --revenue "30Mrd EUR" --profit "5Mrd EUR" --employees 107000
sales-funnel set-hiring "SAP SE" --score 0.7 --total-postings 5000 --reasoning "Stellt aktiv ein"
sales-funnel set-topic-hiring "SAP SE" --topic "Cloud Migration" --score 0.9 --relevant-postings 800 --reasoning "Viele Cloud-Stellen" --positions "Cloud Architect" --positions "DevOps Engineer"
sales-funnel set-strategic "SAP SE" --size-fit 0.5 --financial-health 0.9 --pressure 0.6 --reasoning "Groß, gut situiert, mittlerer Druck"

# Scoring & Export
sales-funnel score [--recalculate]
sales-funnel export [--output results.json] [--format json|csv|markdown]
sales-funnel import leads.json
```

Alle Befehle unterstützen `--file/-f` um eine alternative Leads-Datei anzugeben (default: leads.json).

## Workflow

### Agent 1: Adressgenerator
Wenn der User nach Firmen suchen will:
1. Nutze `WebSearch` um Firmen zu finden die zu den Kriterien passen
2. Für jede gefundene Firma: `sales-funnel add --name "..." --website "..." --industry "..." --address "..."`
3. Zeige die Liste: `sales-funnel list`

### Agent 2: Adressklassifizierer
Für jeden Lead in der Liste:
1. `WebSearch` nach "{Firmenname} news Quartalsbericht" → Firmengesundheit bewerten
2. `WebSearch` nach "{Firmenname} {Thema}" → Themen-Affinität bewerten
3. `sales-funnel set-health "Firma" --score X --reasoning "..." --news "..."`
4. `sales-funnel set-affinity "Firma" --topic "..." --score X --reasoning "..." --news "..."`

### Agent 3: Firmenklassifizierer
Für jeden Lead:
1. `WebSearch` nach "{Firma} Umsatz revenue Mitarbeiter" → Finanzdaten
2. `WebSearch` nach "{Firma} Stellenangebote jobs" → Hiring-Aktivität
3. `WebSearch` nach "{Firma} jobs {Thema}" → Themenbezogene Stellen
4. Setze alle Daten via CLI-Befehle
5. `sales-funnel score` → Berechne Gesamtscores

### Vollständige Pipeline
Alle drei Agenten nacheinander ausführen, dann:
`sales-funnel export --format markdown`

## Tests ausführen

```bash
pytest tests/ -v
```

## Entwicklung

```bash
pip install -e .
```
