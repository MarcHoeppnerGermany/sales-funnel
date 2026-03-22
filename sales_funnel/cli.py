from __future__ import annotations

import argparse
import asyncio
import json
import sys

from dotenv import load_dotenv

from sales_funnel.agents import AddressClassifier, AddressGenerator, CompanyClassifier
from sales_funnel.models.schemas import AgentResult, Company, Lead
from sales_funnel.pipeline import Pipeline


def _load_input_file(path: str) -> AgentResult:
    """Lädt eine JSON-Datei als AgentResult oder als Firmenliste."""
    with open(path) as f:
        data = json.load(f)

    # Versuche als AgentResult zu parsen
    try:
        return AgentResult.model_validate(data)
    except Exception:
        pass

    # Versuche als einfache Firmenliste
    if isinstance(data, list):
        leads = [
            Lead(company=Company.model_validate(c) if isinstance(c, dict) else c)
            for c in data
        ]
        return AgentResult(agent_name="input", leads=leads)

    raise ValueError(f"Kann Datei {path} nicht als Firmenliste interpretieren")


def _output_result(result: AgentResult, output_path: str | None) -> None:
    text = result.model_dump_json(indent=2)
    if output_path:
        with open(output_path, "w") as f:
            f.write(text)
        print(f"Ergebnis gespeichert: {output_path}", file=sys.stderr)
    else:
        print(text)


def cmd_generate(args: argparse.Namespace) -> None:
    """Adressgenerator (Agent 1)."""
    criteria = {
        "industry": args.industry,
        "topics": [t.strip() for t in args.topics.split(",")] if args.topics else [],
        "location": args.location,
        "max_results": args.max_results,
    }

    agent = AddressGenerator()
    result = asyncio.run(agent.run(criteria))
    _output_result(result, args.output)


def cmd_classify_topic(args: argparse.Namespace) -> None:
    """Adressklassifizierer (Agent 2)."""
    if args.input:
        input_data = _load_input_file(args.input)
    else:
        print("Fehler: --input ist erforderlich", file=sys.stderr)
        sys.exit(1)

    agent = AddressClassifier(topic=args.topic)
    result = asyncio.run(agent.run(input_data))
    _output_result(result, args.output)


def cmd_classify_company(args: argparse.Namespace) -> None:
    """Firmenklassifizierer (Agent 3)."""
    if args.input:
        input_data = _load_input_file(args.input)
    else:
        print("Fehler: --input ist erforderlich", file=sys.stderr)
        sys.exit(1)

    agent = CompanyClassifier(context=args.context)
    result = asyncio.run(agent.run(input_data))
    _output_result(result, args.output)


def cmd_pipeline(args: argparse.Namespace) -> None:
    """Vollständige Pipeline oder Teilpipeline."""
    agents = []
    initial_input: dict | AgentResult | None = None

    if args.input:
        initial_input = _load_input_file(args.input)
    else:
        # Agent 1 einschalten
        agents.append(AddressGenerator())
        initial_input = {
            "industry": args.industry,
            "topics": [t.strip() for t in args.topics.split(",")] if args.topics else [],
            "location": args.location,
            "max_results": args.max_results,
        }

    if args.topic:
        agents.append(AddressClassifier(topic=args.topic))

    if not args.skip_company:
        agents.append(CompanyClassifier(context=args.context or args.topic or ""))

    if not agents:
        print("Fehler: Keine Agenten in der Pipeline", file=sys.stderr)
        sys.exit(1)

    pipe = Pipeline(agents)
    print(pipe.describe(), file=sys.stderr)
    result = asyncio.run(pipe.run(initial_input))
    _output_result(result, args.output)


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="sales-funnel",
        description="Sales Lead Generator mit autonomen Agenten",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- generate ---
    p_gen = sub.add_parser("generate", help="Adressen generieren (Agent 1)")
    p_gen.add_argument("--industry", default="Software", help="Branche")
    p_gen.add_argument("--topics", default="", help="Themen, kommagetrennt")
    p_gen.add_argument("--location", default="Deutschland", help="Region")
    p_gen.add_argument("--max-results", type=int, default=20, help="Max Ergebnisse")
    p_gen.add_argument("--output", "-o", help="Ausgabedatei (JSON)")
    p_gen.set_defaults(func=cmd_generate)

    # --- classify-topic ---
    p_cls = sub.add_parser("classify-topic", help="Nach Thema klassifizieren (Agent 2)")
    p_cls.add_argument("--input", "-i", required=True, help="Eingabedatei (JSON)")
    p_cls.add_argument("--topic", "-t", required=True, help="Thema zur Bewertung")
    p_cls.add_argument("--output", "-o", help="Ausgabedatei (JSON)")
    p_cls.set_defaults(func=cmd_classify_topic)

    # --- classify-company ---
    p_cmp = sub.add_parser("classify-company", help="Firma bewerten (Agent 3)")
    p_cmp.add_argument("--input", "-i", required=True, help="Eingabedatei (JSON)")
    p_cmp.add_argument("--context", default="Softwareentwicklung", help="Unser Angebot")
    p_cmp.add_argument("--output", "-o", help="Ausgabedatei (JSON)")
    p_cmp.set_defaults(func=cmd_classify_company)

    # --- pipeline ---
    p_pipe = sub.add_parser("pipeline", help="Agenten-Pipeline ausführen")
    p_pipe.add_argument("--input", "-i", help="Eingabedatei (überspringt Agent 1)")
    p_pipe.add_argument("--industry", default="Software", help="Branche")
    p_pipe.add_argument("--topics", default="", help="Themen, kommagetrennt")
    p_pipe.add_argument("--location", default="Deutschland", help="Region")
    p_pipe.add_argument("--max-results", type=int, default=20, help="Max Ergebnisse")
    p_pipe.add_argument("--topic", "-t", help="Thema für Klassifizierung")
    p_pipe.add_argument("--context", help="Kontext für Firmenbewertung")
    p_pipe.add_argument("--skip-company", action="store_true", help="Agent 3 überspringen")
    p_pipe.add_argument("--output", "-o", help="Ausgabedatei (JSON)")
    p_pipe.set_defaults(func=cmd_pipeline)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
