# Sales Lead Generator

Dieses Projekt nutzt Claude Code als AI-Engine für die Lead-Generierung.
Die Python-CLI (`sales-funnel`) verwaltet Daten, Scoring und Export.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

## Workflow Orchestration

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately – don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

**Verbindliche Agent-Regeln für Lead-Recherche (seit 2026-05):**
- **Read-only-Vertrag**: Agenten recherchieren nur (WebSearch) und geben
  strukturiertes JSON zurück. Sie schreiben NIEMALS selbst in `leads.json`.
- **Max. 8 Firmen pro Agent** — größere Aufträge timeouten (Lesson: 19er-Batch
  starb nach 30 Min). Lieber 3 kleine Agenten parallel.
- **Persistierung nur zentral** über `scripts/apply_scores.py` — der einzige
  Schreibpfad, Schema-validiert via Pydantic + offizielle Scoring-Formeln.
- **Validierungs-Gate** `scripts/validate_leads.py` nach jedem Schreiben und
  vor jedem Export (Exporte brechen bei rotem Gate automatisch ab).
- Geschätzte Werte im reasoning als "(geschätzt)" kennzeichnen.

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "Is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes – don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests – then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

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

## Agent-Workflows

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

## Tests ausführen

```bash
pytest tests/ -v
```

## Entwicklung

```bash
pip install -e .
```
