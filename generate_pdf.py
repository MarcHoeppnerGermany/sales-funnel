#!/usr/bin/env python3
"""PDF-Lead-Sheets — liest AUSSCHLIESSLICH aus leads.json.

Enthalten: alle TIER1-Leads + Top 5 je Pipeline (Fernwaerme, Energiehandel,
Telematik). Vorher läuft das Validierungs-Gate.
"""
import json
import subprocess
import sys

from fpdf import FPDF

TOP_N_PER_PIPELINE = 5
EXTRA_PIPELINES = ["Fernwaerme", "Energiehandel", "Telematik"]


class LeadPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "neogeo systems - Lead Sheet (vertraulich)", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def section(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(41, 65, 122)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f"  {title}", fill=True)
        self.ln(9)
        self.set_text_color(0, 0, 0)

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 9)
        self.cell(52, 6, key + ":")
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 6, safe(val) if val else "k.A.")
        self.ln(1)

    def score_bar(self, label, score, w=60):
        score = score or 0
        self.set_font("Helvetica", "", 9)
        self.cell(52, 6, label + ":")
        x, y = self.get_x(), self.get_y()
        self.set_fill_color(220, 220, 220)
        self.rect(x, y, w, 5, "F")
        if score >= 0.7:
            self.set_fill_color(46, 139, 87)
        elif score >= 0.5:
            self.set_fill_color(218, 165, 32)
        else:
            self.set_fill_color(178, 34, 34)
        self.rect(x, y, w * score, 5, "F")
        self.set_xy(x + w + 3, y)
        self.cell(20, 6, f"{score:.0%}")
        self.ln(7)


def safe(text, maxlen=600):
    if text is None:
        return "k.A."
    t = str(text)
    for a, b in [("–", "-"), ("—", "-"), ("‘", "'"), ("’", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " "),
                 ("→", "->"), ("²", "2"), ("€", "EUR")]:
        t = t.replace(a, b)
    t = t.encode("latin-1", errors="replace").decode("latin-1")
    return t[:maxlen] + ("..." if len(t) > maxlen else "")


def render_lead(pdf, lead):
    co = lead["company"]
    tr = lead.get("topic_relevance") or {}
    fin = lead.get("financials") or {}
    sf = fin.get("strategic_fit") or {}
    health = tr.get("company_health") or {}
    affinity = tr.get("topic_affinity") or {}
    outreach = lead.get("outreach") or {}

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(41, 65, 122)
    pdf.cell(0, 10, safe(co["name"], 80))
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    meta = " | ".join(filter(None, [
        lead.get("pipeline"), lead.get("tier"),
        co.get("industry"), co.get("address"),
    ]))
    pdf.cell(0, 6, safe(meta, 110))
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)

    score = lead.get("overall_score") or 0
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(35, 8, "Overall Score:")
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*(46, 139, 87) if score >= 0.7 else (218, 165, 32) if score >= 0.5 else (178, 34, 34))
    pdf.cell(20, 8, f"{score:.1%}")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 8, f"    Customer Rating: {fin.get('customer_rating', 0) or 0:.0%}")
    pdf.ln(12)

    pdf.section("Stammdaten")
    pdf.kv("Website", co.get("website"))
    pdf.kv("Umsatz", fin.get("revenue_estimate"))
    pdf.kv("Mitarbeiter", fin.get("employee_count"))
    pdf.ln(3)

    pdf.section("Scoring")
    pdf.score_bar("Firmengesundheit", health.get("activity_score"))
    pdf.score_bar("Themen-Affinitaet", affinity.get("affinity_score"))
    pdf.score_bar("Size Fit", sf.get("size_fit_score"))
    pdf.score_bar("Marktdruck", sf.get("pressure_score"))
    pdf.score_bar("Hiring allg.", (fin.get("hiring_activity") or {}).get("general_hiring_score"))
    pdf.score_bar("Topic Hiring", (fin.get("topic_hiring") or {}).get("topic_hiring_score"))
    pdf.ln(3)

    if sf.get("strategic_reasoning"):
        pdf.section("Strategische Einschaetzung")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, safe(sf["strategic_reasoning"]))
        pdf.ln(3)

    contacts = lead.get("contact_persons") or []
    if contacts:
        pdf.section("Ansprechpartner")
        for c in contacts:
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(55, 6, safe(c["name"], 40))
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(95, 6, safe(c.get("role"), 65))
            conf = c.get("confidence") or ""
            pdf.set_text_color(*(46, 139, 87) if conf == "HIGH" else (218, 165, 32) if conf == "MEDIUM" else (178, 34, 34))
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, conf)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(7)
        pdf.ln(3)

    if outreach.get("subject"):
        pdf.section("Outreach-Vorlage")
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(18, 6, "Betreff:")
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(0, 6, safe(outreach["subject"]))
        pdf.ln(2)
        if outreach.get("hook"):
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(22, 6, "Aufhaenger:")
            pdf.set_font("Helvetica", "", 9)
            pdf.multi_cell(0, 5, safe(outreach["hook"]))


def main():
    gate = subprocess.run(
        [sys.executable, "scripts/validate_leads.py"], capture_output=True, text=True
    )
    if gate.returncode != 0:
        print(gate.stdout)
        sys.exit("ABBRUCH: Validierungs-Gate fehlgeschlagen.")

    with open("leads.json") as f:
        leads = json.load(f)["leads"]

    tier1 = sorted(
        [l for l in leads if l.get("tier") == "TIER1"],
        key=lambda x: -(x.get("overall_score") or 0),
    )
    selected = list(tier1)
    for pipeline in EXTRA_PIPELINES:
        top = sorted(
            [l for l in leads if l.get("pipeline") == pipeline],
            key=lambda x: -(x.get("overall_score") or 0),
        )[:TOP_N_PER_PIPELINE]
        selected.extend(top)

    pdf = LeadPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(41, 65, 122)
    pdf.cell(0, 15, "Lead Sheets", align="C")
    pdf.ln(18)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, f"IoT TIER 1 ({len(tier1)}) + Top {TOP_N_PER_PIPELINE} je Pipeline", align="C")
    pdf.ln(10)
    pdf.cell(0, 8, ", ".join(EXTRA_PIPELINES), align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, "Generiert aus leads.json | Vertraulich", align="C")

    for lead in selected:
        render_lead(pdf, lead)

    out = "iot_lead_sheets.pdf"
    pdf.output(out)
    print(f"PDF erstellt: {out} ({pdf.page_no()} Seiten, {len(selected)} Leads)")


if __name__ == "__main__":
    main()
