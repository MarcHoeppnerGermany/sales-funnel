from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

from sales_funnel.models.schemas import (
    Company,
    CompanyFinancials,
    CompanyHealth,
    HiringActivity,
    Lead,
    StrategicFit,
    TopicAffinity,
    TopicHiring,
)
from sales_funnel.scoring import rank_leads, score_customer_rating, score_topic_relevance
from sales_funnel.store import LeadStore


def _store(args: argparse.Namespace) -> LeadStore:
    return LeadStore(path=getattr(args, "file", "leads.json"))


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace) -> None:
    store = _store(args)

    if args.from_json:
        path = Path(args.from_json)
        if not path.exists():
            _err(f"Datei nicht gefunden: {path}")
            sys.exit(1)
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            _err("JSON-Datei muss eine Liste von Firmen-Objekten sein")
            sys.exit(1)
        leads = []
        for item in data:
            if isinstance(item, dict):
                company = Company.model_validate(item)
            else:
                _err(f"Ungültiger Eintrag: {item}")
                continue
            leads.append(Lead(company=company))
        result = store.add_leads(leads)
        _err(f"{len(leads)} Leads importiert, {len(result.leads)} gesamt.")
        return

    if not args.name:
        _err("--name ist erforderlich (oder --from-json)")
        sys.exit(1)

    company = Company(
        name=args.name,
        website=args.website,
        industry=args.industry,
        address=args.address,
        source=args.source,
    )
    lead = Lead(company=company)
    result = store.add_leads([lead])
    _err(f"Lead hinzugefügt: {company.name} ({len(result.leads)} gesamt)")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> None:
    store = _store(args)
    result = store.load()
    leads = result.leads

    if not leads:
        _err("Keine Leads vorhanden.")
        return

    sort_key = getattr(args, "sort", "name")
    if sort_key == "score":
        leads = sorted(leads, key=lambda l: l.overall_score or 0, reverse=True)
    else:
        leads = sorted(leads, key=lambda l: l.company.name.lower())

    fmt = getattr(args, "format", "table")
    if fmt == "json":
        out = json.dumps(
            [lead.model_dump() for lead in leads],
            indent=2,
            ensure_ascii=False,
            default=str,
        )
        print(out)
    else:
        _print_table(leads)


def _print_table(leads: list[Lead]) -> None:
    header = f"{'#':<4} {'Firma':<30} {'Branche':<20} {'Ort':<20} {'Topic':<8} {'Overall':<8}"
    print(header)
    print("-" * len(header))
    for i, lead in enumerate(leads, 1):
        topic = ""
        if lead.topic_relevance:
            topic = f"{lead.topic_relevance.combined_score:.2f}"
        overall = ""
        if lead.overall_score is not None:
            overall = f"{lead.overall_score:.3f}"
        print(
            f"{i:<4} "
            f"{lead.company.name[:29]:<30} "
            f"{(lead.company.industry or '-')[:19]:<20} "
            f"{(lead.company.address or '-')[:19]:<20} "
            f"{topic:<8} "
            f"{overall:<8}"
        )


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------

def cmd_show(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)
    print(lead.model_dump_json(indent=2))


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------

def cmd_remove(args: argparse.Namespace) -> None:
    store = _store(args)
    if store.remove_lead(args.name):
        _err(f"Lead entfernt: {args.name}")
    else:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# set-health
# ---------------------------------------------------------------------------

def cmd_set_health(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)

    health = CompanyHealth(
        activity_score=args.score,
        activity_reasoning=args.reasoning,
        recent_news=args.news or [],
    )

    # If there's already a topic_relevance, update its health; otherwise create one
    if lead.topic_relevance:
        relevance = score_topic_relevance(health, lead.topic_relevance.topic_affinity)
    else:
        # Store health, will combine when affinity is set
        from sales_funnel.models.schemas import TopicAffinity as TA, TopicRelevance as TR

        relevance = TR(
            company_health=health,
            topic_affinity=TA(
                topic="(nicht gesetzt)",
                affinity_score=0.0,
                affinity_reasoning="Noch nicht bewertet",
            ),
            combined_score=round(health.activity_score * 0.4, 3),
        )

    store.update_lead(args.name, topic_relevance=relevance)
    _err(f"Health gesetzt für {args.name}: {args.score}")


# ---------------------------------------------------------------------------
# set-affinity
# ---------------------------------------------------------------------------

def cmd_set_affinity(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)

    affinity = TopicAffinity(
        topic=args.topic,
        affinity_score=args.score,
        affinity_reasoning=args.reasoning,
        relevant_news=args.news or [],
    )

    if lead.topic_relevance:
        relevance = score_topic_relevance(lead.topic_relevance.company_health, affinity)
    else:
        from sales_funnel.models.schemas import TopicRelevance as TR

        health = CompanyHealth(
            activity_score=0.0,
            activity_reasoning="Noch nicht bewertet",
        )
        relevance = TR(
            company_health=health,
            topic_affinity=affinity,
            combined_score=round(affinity.affinity_score * 0.6, 3),
        )

    store.update_lead(args.name, topic_relevance=relevance)
    _err(f"Affinity gesetzt für {args.name}: {args.topic} = {args.score}")


# ---------------------------------------------------------------------------
# set-financials
# ---------------------------------------------------------------------------

def cmd_set_financials(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)

    fin = lead.financials or CompanyFinancials()
    fin = fin.model_copy(
        update={
            "revenue_estimate": args.revenue or fin.revenue_estimate,
            "profit_estimate": args.profit or fin.profit_estimate,
            "employee_count": args.employees or fin.employee_count,
        }
    )
    store.update_lead(args.name, financials=fin)
    _err(f"Finanzdaten gesetzt für {args.name}")


# ---------------------------------------------------------------------------
# set-hiring
# ---------------------------------------------------------------------------

def cmd_set_hiring(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)

    hiring = HiringActivity(
        general_hiring_score=args.score,
        total_job_postings=args.total_postings,
        hiring_reasoning=args.reasoning,
    )

    fin = lead.financials or CompanyFinancials()
    fin = fin.model_copy(update={"hiring_activity": hiring})
    store.update_lead(args.name, financials=fin)
    _err(f"Hiring gesetzt für {args.name}: {args.score}")


# ---------------------------------------------------------------------------
# set-topic-hiring
# ---------------------------------------------------------------------------

def cmd_set_topic_hiring(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)

    topic_hiring = TopicHiring(
        topic_hiring_score=args.score,
        relevant_job_postings=args.relevant_postings,
        topic_hiring_reasoning=args.reasoning,
        example_positions=args.positions or [],
    )

    fin = lead.financials or CompanyFinancials()
    fin = fin.model_copy(update={"topic_hiring": topic_hiring})
    store.update_lead(args.name, financials=fin)
    _err(f"Topic-Hiring gesetzt für {args.name}: {args.score}")


# ---------------------------------------------------------------------------
# set-strategic
# ---------------------------------------------------------------------------

def cmd_set_strategic(args: argparse.Namespace) -> None:
    store = _store(args)
    lead = store.get_lead(args.name)
    if not lead:
        _err(f"Lead nicht gefunden: {args.name}")
        sys.exit(1)

    strategic = StrategicFit(
        size_fit_score=args.size_fit,
        financial_health_score=args.financial_health,
        pressure_score=args.pressure,
        strategic_reasoning=args.reasoning,
    )

    fin = lead.financials or CompanyFinancials()
    # Recalculate customer_rating if we have enough data
    hiring_score = fin.hiring_activity.general_hiring_score if fin.hiring_activity else 0.0
    topic_hiring_score = fin.topic_hiring.topic_hiring_score if fin.topic_hiring else 0.0
    rating = score_customer_rating(
        hiring_score, topic_hiring_score, strategic.pressure_score, strategic.size_fit_score
    )
    fin = fin.model_copy(
        update={
            "strategic_fit": strategic,
            "customer_rating": rating,
            "rating_reasoning": strategic.strategic_reasoning,
        }
    )
    store.update_lead(args.name, financials=fin)
    _err(f"Strategic Fit gesetzt für {args.name}: size={args.size_fit}, pressure={args.pressure}")


# ---------------------------------------------------------------------------
# score
# ---------------------------------------------------------------------------

def cmd_score(args: argparse.Namespace) -> None:
    store = _store(args)
    result = store.load()
    if not result.leads:
        _err("Keine Leads vorhanden.")
        return

    ranked = rank_leads(result.leads)
    result.leads = ranked
    store.save(result)

    _err(f"Scores berechnet für {len(ranked)} Leads:")
    for i, lead in enumerate(ranked, 1):
        _err(f"  {i}. {lead.company.name}: {lead.overall_score:.3f}")


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------

def cmd_export(args: argparse.Namespace) -> None:
    store = _store(args)
    result = store.load()
    if not result.leads:
        _err("Keine Leads vorhanden.")
        return

    fmt = getattr(args, "format", "json")
    output_text = ""

    if fmt == "json":
        output_text = json.dumps(
            [lead.model_dump() for lead in result.leads],
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    elif fmt == "csv":
        output_text = _export_csv(result.leads)
    elif fmt == "markdown":
        output_text = _export_markdown(result.leads)

    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
        _err(f"Export gespeichert: {args.output}")
    else:
        print(output_text)


def _export_csv(leads: list[Lead]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "Firma", "Website", "Branche", "Ort",
        "Health Score", "Affinity Score", "Topic Score",
        "Hiring Score", "Topic Hiring Score",
        "Size Fit", "Financial Health", "Pressure",
        "Customer Rating", "Overall Score",
    ])
    for lead in leads:
        tr = lead.topic_relevance
        fin = lead.financials
        writer.writerow([
            lead.company.name,
            lead.company.website or "",
            lead.company.industry or "",
            lead.company.address or "",
            tr.company_health.activity_score if tr else "",
            tr.topic_affinity.affinity_score if tr else "",
            tr.combined_score if tr else "",
            fin.hiring_activity.general_hiring_score if fin and fin.hiring_activity else "",
            fin.topic_hiring.topic_hiring_score if fin and fin.topic_hiring else "",
            fin.strategic_fit.size_fit_score if fin and fin.strategic_fit else "",
            fin.strategic_fit.financial_health_score if fin and fin.strategic_fit else "",
            fin.strategic_fit.pressure_score if fin and fin.strategic_fit else "",
            fin.customer_rating if fin else "",
            lead.overall_score if lead.overall_score is not None else "",
        ])
    return buf.getvalue()


def _export_markdown(leads: list[Lead]) -> str:
    lines = ["# Sales Leads Report", ""]

    for i, lead in enumerate(leads, 1):
        c = lead.company
        lines.append(f"## {i}. {c.name}")
        lines.append("")
        if c.website:
            lines.append(f"- **Website:** {c.website}")
        if c.industry:
            lines.append(f"- **Branche:** {c.industry}")
        if c.address:
            lines.append(f"- **Ort:** {c.address}")
        if lead.overall_score is not None:
            lines.append(f"- **Overall Score:** {lead.overall_score:.3f}")
        lines.append("")

        tr = lead.topic_relevance
        if tr:
            lines.append("### Themenrelevanz")
            lines.append("")
            h = tr.company_health
            lines.append(f"- **Firmengesundheit:** {h.activity_score:.2f} - {h.activity_reasoning}")
            if h.recent_news:
                for news in h.recent_news:
                    lines.append(f"  - {news}")
            a = tr.topic_affinity
            lines.append(f"- **Themen-Affinität ({a.topic}):** {a.affinity_score:.2f} - {a.affinity_reasoning}")
            if a.relevant_news:
                for news in a.relevant_news:
                    lines.append(f"  - {news}")
            lines.append(f"- **Combined Score:** {tr.combined_score:.3f}")
            lines.append("")

        fin = lead.financials
        if fin:
            lines.append("### Firmenbewertung")
            lines.append("")
            if fin.revenue_estimate:
                lines.append(f"- **Umsatz:** {fin.revenue_estimate}")
            if fin.profit_estimate:
                lines.append(f"- **Gewinn:** {fin.profit_estimate}")
            if fin.employee_count:
                lines.append(f"- **Mitarbeiter:** {fin.employee_count}")

            if fin.hiring_activity:
                ha = fin.hiring_activity
                lines.append(f"- **Hiring:** {ha.general_hiring_score:.2f} - {ha.hiring_reasoning}")
                if ha.total_job_postings:
                    lines.append(f"  - {ha.total_job_postings} Stellenanzeigen")

            if fin.topic_hiring:
                th = fin.topic_hiring
                lines.append(f"- **Topic Hiring:** {th.topic_hiring_score:.2f} - {th.topic_hiring_reasoning}")
                if th.relevant_job_postings:
                    lines.append(f"  - {th.relevant_job_postings} relevante Stellen")
                if th.example_positions:
                    lines.append(f"  - Positionen: {', '.join(th.example_positions)}")

            if fin.strategic_fit:
                sf = fin.strategic_fit
                lines.append(f"- **Strategic Fit:**")
                lines.append(f"  - Size Fit: {sf.size_fit_score:.2f}")
                lines.append(f"  - Financial Health: {sf.financial_health_score:.2f}")
                lines.append(f"  - Pressure: {sf.pressure_score:.2f}")
                lines.append(f"  - {sf.strategic_reasoning}")

            lines.append(f"- **Customer Rating:** {fin.customer_rating:.3f}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# import
# ---------------------------------------------------------------------------

def cmd_import(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if not path.exists():
        _err(f"Datei nicht gefunden: {path}")
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    store = _store(args)

    # Try to parse as AgentResult first
    from sales_funnel.models.schemas import AgentResult

    try:
        ar = AgentResult.model_validate(data)
        result = store.add_leads(ar.leads)
        _err(f"{len(ar.leads)} Leads importiert aus AgentResult, {len(result.leads)} gesamt.")
        return
    except Exception:
        pass

    # Try as list of leads
    if isinstance(data, list):
        leads = []
        for item in data:
            if isinstance(item, dict):
                if "company" in item:
                    leads.append(Lead.model_validate(item))
                else:
                    leads.append(Lead(company=Company.model_validate(item)))
        result = store.add_leads(leads)
        _err(f"{len(leads)} Leads importiert, {len(result.leads)} gesamt.")
        return

    _err("Kann Datei nicht als Leads-Datei interpretieren.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# main / argparse
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sales-funnel",
        description="Sales Lead Generator - Datenverwaltung & Scoring",
    )
    parser.add_argument(
        "--file", "-f", default="leads.json", help="Leads-Datei (default: leads.json)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- add ---
    p_add = sub.add_parser("add", help="Lead hinzufügen")
    p_add.add_argument("--name", help="Firmenname")
    p_add.add_argument("--website", help="Website")
    p_add.add_argument("--industry", help="Branche")
    p_add.add_argument("--address", help="Adresse/Ort")
    p_add.add_argument("--source", help="Quelle")
    p_add.add_argument("--from-json", help="JSON-Datei mit Firmenliste importieren")
    p_add.set_defaults(func=cmd_add)

    # --- list ---
    p_list = sub.add_parser("list", help="Leads auflisten")
    p_list.add_argument("--format", choices=["table", "json"], default="table")
    p_list.add_argument("--sort", choices=["score", "name"], default="name")
    p_list.set_defaults(func=cmd_list)

    # --- show ---
    p_show = sub.add_parser("show", help="Lead anzeigen")
    p_show.add_argument("name", help="Firmenname")
    p_show.set_defaults(func=cmd_show)

    # --- remove ---
    p_rm = sub.add_parser("remove", help="Lead entfernen")
    p_rm.add_argument("name", help="Firmenname")
    p_rm.set_defaults(func=cmd_remove)

    # --- set-health ---
    p_health = sub.add_parser("set-health", help="Firmengesundheit setzen")
    p_health.add_argument("name", help="Firmenname")
    p_health.add_argument("--score", type=float, required=True, help="Activity Score (0-1)")
    p_health.add_argument("--reasoning", required=True, help="Begründung")
    p_health.add_argument("--news", action="append", help="Aktuelle News (mehrfach)")
    p_health.set_defaults(func=cmd_set_health)

    # --- set-affinity ---
    p_aff = sub.add_parser("set-affinity", help="Themen-Affinität setzen")
    p_aff.add_argument("name", help="Firmenname")
    p_aff.add_argument("--topic", required=True, help="Thema")
    p_aff.add_argument("--score", type=float, required=True, help="Affinity Score (0-1)")
    p_aff.add_argument("--reasoning", required=True, help="Begründung")
    p_aff.add_argument("--news", action="append", help="Relevante News (mehrfach)")
    p_aff.set_defaults(func=cmd_set_affinity)

    # --- set-financials ---
    p_fin = sub.add_parser("set-financials", help="Finanzdaten setzen")
    p_fin.add_argument("name", help="Firmenname")
    p_fin.add_argument("--revenue", help="Umsatzschätzung")
    p_fin.add_argument("--profit", help="Gewinnschätzung")
    p_fin.add_argument("--employees", type=int, help="Mitarbeiterzahl")
    p_fin.set_defaults(func=cmd_set_financials)

    # --- set-hiring ---
    p_hire = sub.add_parser("set-hiring", help="Hiring-Aktivität setzen")
    p_hire.add_argument("name", help="Firmenname")
    p_hire.add_argument("--score", type=float, required=True, help="Hiring Score (0-1)")
    p_hire.add_argument("--total-postings", type=int, help="Gesamtzahl Stellenanzeigen")
    p_hire.add_argument("--reasoning", required=True, help="Begründung")
    p_hire.set_defaults(func=cmd_set_hiring)

    # --- set-topic-hiring ---
    p_th = sub.add_parser("set-topic-hiring", help="Themenbezogene Stellen setzen")
    p_th.add_argument("name", help="Firmenname")
    p_th.add_argument("--score", type=float, required=True, help="Topic Hiring Score (0-1)")
    p_th.add_argument("--relevant-postings", type=int, help="Relevante Stellenanzeigen")
    p_th.add_argument("--reasoning", required=True, help="Begründung")
    p_th.add_argument("--positions", action="append", help="Beispiel-Positionen (mehrfach)")
    p_th.set_defaults(func=cmd_set_topic_hiring)

    # --- set-strategic ---
    p_strat = sub.add_parser("set-strategic", help="Strategischen Fit setzen")
    p_strat.add_argument("name", help="Firmenname")
    p_strat.add_argument("--size-fit", type=float, required=True, help="Size Fit Score (0-1)")
    p_strat.add_argument("--financial-health", type=float, required=True, help="Financial Health (0-1)")
    p_strat.add_argument("--pressure", type=float, required=True, help="Pressure Score (0-1)")
    p_strat.add_argument("--reasoning", required=True, help="Begründung")
    p_strat.set_defaults(func=cmd_set_strategic)

    # --- score ---
    p_score = sub.add_parser("score", help="Scores berechnen")
    p_score.add_argument("--recalculate", action="store_true", help="Alle Scores neu berechnen")
    p_score.set_defaults(func=cmd_score)

    # --- export ---
    p_export = sub.add_parser("export", help="Leads exportieren")
    p_export.add_argument("--output", "-o", help="Ausgabedatei")
    p_export.add_argument("--format", choices=["json", "csv", "markdown"], default="json")
    p_export.set_defaults(func=cmd_export)

    # --- import ---
    p_import = sub.add_parser("import", help="Leads importieren")
    p_import.add_argument("path", help="Pfad zur JSON-Datei")
    p_import.set_defaults(func=cmd_import)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
