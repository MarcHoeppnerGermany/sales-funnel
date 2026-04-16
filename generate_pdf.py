#!/usr/bin/env python3
"""Generate PDF lead sheets for all IoT TIER 1 leads."""
import json
from fpdf import FPDF

class LeadPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'neogeo systems - IoT Lead Sheet (vertraulich)', align='R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Seite {self.page_no()}/{{nb}}', align='C')

    def section(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(41, 65, 122)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f'  {title}', fill=True)
        self.ln(9)
        self.set_text_color(0, 0, 0)

    def kv(self, key, val):
        self.set_font('Helvetica', 'B', 9)
        self.cell(52, 6, key + ':')
        self.set_font('Helvetica', '', 9)
        # Handle long values with multi_cell
        x = self.get_x()
        y = self.get_y()
        self.multi_cell(0, 6, str(val) if val else 'k.A.')
        if self.get_y() == y + 6:
            pass  # single line, already advanced
        self.ln(1)

    def score_bar(self, label, score, w=60):
        self.set_font('Helvetica', '', 9)
        self.cell(52, 6, label + ':')
        x = self.get_x()
        y = self.get_y()
        # Background
        self.set_fill_color(220, 220, 220)
        self.rect(x, y, w, 5, 'F')
        # Score bar
        if score >= 0.7:
            self.set_fill_color(46, 139, 87)
        elif score >= 0.5:
            self.set_fill_color(218, 165, 32)
        else:
            self.set_fill_color(178, 34, 34)
        self.rect(x, y, w * score, 5, 'F')
        # Text
        self.set_xy(x + w + 3, y)
        self.cell(20, 6, f'{score:.0%}')
        self.ln(7)


def safe(text, maxlen=500):
    """Ensure text is safe for fpdf."""
    if not text:
        return 'k.A.'
    t = str(text)
    # Replace problematic chars
    t = t.replace('\u2013', '-').replace('\u2014', '-')
    t = t.replace('\u2018', "'").replace('\u2019', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = t.replace('\u2026', '...')
    t = t.replace('\u00a0', ' ')
    t = t.replace('\u2192', '->')
    t = t.replace('\u2191', '^')
    t = t.replace('\u00b2', '2')  # superscript 2
    # Encode to latin-1 safe
    t = t.encode('latin-1', errors='replace').decode('latin-1')
    if len(t) > maxlen:
        t = t[:maxlen] + '...'
    return t


# Outreach data (from iot_outreach_templates.md)
OUTREACH = {
    'Rosenberger Hochfrequenztechnik': {
        'betreff': 'Vom CISO zum CIO bei Rosenberger - wie weit ist der IoT-Kern?',
        'aufhaenger': 'CISO->CIO Wechsel in 18 Monaten, "IT als Business Enabler", CISSP + MBA IT Mgmt',
    },
    'Mekra Lang GmbH': {
        'betreff': 'Kamerasysteme, Digital-Business-Thesis und IoT - passt das zusammen?',
        'aufhaenger': 'Studiert Master Digital Business Mgmt neben dem Job. MEKRA View = IoT-Produkt.',
    },
    'ACO Severin Ahlmann': {
        'betreff': 'Von HELM zu ACO: Smart Drainage als naechster IoT-Move?',
        'aufhaenger': 'Ex-HELM AG (2012-2019). Entwaesserungstechnik = verteilte, datenlose Infrastruktur.',
    },
    'GP JOULE GmbH': {
        'betreff': 'Wind + PV + H2 unter einem Asset-Dach - wie, Herr Friedrichsen?',
        'aufhaenger': 'Neuer CIO. Wind+PV+H2+E-Mobility = heterogenstes Asset-Portfolio.',
    },
    'Stern-Wywiol Gruppe': {
        'betreff': 'IT/OT in einer Rolle + 12 Firmen: Wo ist der gemeinsame Asset-Kern?',
        'aufhaenger': 'Seltene IT/OT-Doppelrolle. SternConnect Digi-Unit. 12 Spezialfirmen.',
    },
    'Sikora AG': {
        'betreff': 'Sikoras Sensorik trifft Asset-IoT - Austausch auf Augenhoehe?',
        'aufhaenger': 'Sikora ist selbst Sensorhersteller (Roentgen, Laser, Kameras). Sparring auf Augenhoehe.',
    },
    'Nordex SE': {
        'betreff': '6.800 Turbinen + Acciona-SAP: die Nische neben Mindtree?',
        'aufhaenger': 'Cumulocity SCADA, 6.800+ Turbinen, Mindtree-5J-Deal, Acciona-Integration.',
    },
    'SH Netz AG (HanseWerk)': {
        'betreff': '24 Jahre HanseWerk Natur - Gespraech zur LoRaWAN-Asset-Bruecke?',
        'aufhaenger': '24 Jahre HanseWerk Natur! LoRaWAN 60->400 Antennen. Bridge Strom/Waerme.',
    },
    'Harburg-Freudenberger Maschinenbau (HF Group)': {
        'betreff': 'ECM steht - wie nah ist HF Mixing an einer Asset-Schicht?',
        'aufhaenger': '71 MA IT, ECM mit ACTIWARE/ELO, 4 Business Units mit versch. Maschinenparks.',
    },
    'Fritz Winter Eisengie\u00dferei': {
        'betreff': 'Nach 75% IT-Leerlauf: Was macht der Asset-Kern jetzt?',
        'aufhaenger': 'CIO.de-Feature Feb 2026 "75% IT-Leerlauf". NetApp uSCALE. SAP konsolidiert.',
    },
    'Klosterfrau Healthcare Group': {
        'betreff': '2002-heute: Aehnliche Langstrecke - Asset-IoT fuer Berlin/Luechow?',
        'aufhaenger': 'CIO seit 2002 (24 Jahre wie wir!). S/4HANA seit 2021. Picavi Smart Glasses.',
    },
}

# Contact persons (from iot_kontaktliste.md research)
CONTACTS = {
    'Rosenberger Hochfrequenztechnik': [
        {'name': 'Walter Hoelblinger, MBA', 'role': 'CIO / Global Head of IT (seit Jan 2025)', 'conf': 'HIGH'},
    ],
    'Mekra Lang GmbH': [
        {'name': 'Michael Ammon', 'role': 'Global Head of IT', 'conf': 'HIGH'},
        {'name': 'Jorge Calderon', 'role': 'IT Manager (Direct Report)', 'conf': 'MEDIUM'},
    ],
    'ACO Severin Ahlmann': [
        {'name': 'Dominik Neff', 'role': 'CIO, ACO Group (seit Sep 2022)', 'conf': 'HIGH'},
        {'name': 'Stephan Bauer', 'role': 'Leiter IT Service Management', 'conf': 'MEDIUM'},
    ],
    'GP JOULE GmbH': [
        {'name': 'Kerrit Friedrichsen', 'role': 'CIO, GP JOULE Gruppe', 'conf': 'HIGH'},
    ],
    'Stern-Wywiol Gruppe': [
        {'name': 'Kay Postwig', 'role': 'Head of IT/OT', 'conf': 'HIGH'},
    ],
    'Sikora AG': [
        {'name': 'Christoph Hueniken', 'role': 'IT-Leiter, Sikora Holding', 'conf': 'HIGH'},
    ],
    'Nordex SE': [
        {'name': 'Stefan Ewald', 'role': 'CIO, Head of IT & Organization', 'conf': 'HIGH'},
        {'name': 'Volker Scheeff', 'role': 'Director Corporate IT ERP', 'conf': 'MEDIUM'},
    ],
    'SH Netz AG (HanseWerk)': [
        {'name': 'Thorsten Frye', 'role': 'CIO & CDO, HanseWerk', 'conf': 'HIGH'},
        {'name': 'Lisa Hebenstreit', 'role': 'GF Netztechnik SH Netz (Ex-Head Digital & IT)', 'conf': 'HIGH'},
    ],
    'Harburg-Freudenberger Maschinenbau (HF Group)': [
        {'name': 'Alexander Bodi', 'role': 'Head of IT (71 MA)', 'conf': 'HIGH'},
    ],
    'Fritz Winter Eisengie\u00dferei': [
        {'name': 'Alexander Schwab', 'role': 'Leiter IT und Digitalisierung', 'conf': 'HIGH'},
    ],
    'Klosterfrau Healthcare Group': [
        {'name': 'Frank Roth', 'role': 'CIO / Leiter Shared Service Center IT (seit 2002)', 'conf': 'HIGH'},
    ],
}


def main():
    with open('leads.json') as f:
        data = json.load(f)

    # Filter TIER 1 leads
    tier1_names = list(OUTREACH.keys())
    tier1_leads = []
    for lead in data['leads']:
        if lead['company']['name'] in tier1_names:
            tier1_leads.append(lead)

    # Sort by overall_score descending
    tier1_leads.sort(key=lambda x: -(x.get('overall_score') or 0))

    pdf = LeadPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title page
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(41, 65, 122)
    pdf.cell(0, 15, 'IoT Lead Sheets', align='C')
    pdf.ln(18)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'TIER 1 - HOT LEADS', align='C')
    pdf.ln(12)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, '11 personalisierte Lead-Profile mit Scores,', align='C')
    pdf.ln(8)
    pdf.cell(0, 8, 'Ansprechpartnern und Outreach-Vorlagen', align='C')
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, 'Stand: 15.04.2026 | Vertraulich', align='C')

    # One page per lead
    for lead in tier1_leads:
        co = lead['company']
        name = co['name']
        tr = lead.get('topic_relevance') or {}
        fin = lead.get('financials') or {}
        sf = fin.get('strategic_fit') or {}
        health = (tr.get('company_health') or {})
        affinity = (tr.get('topic_affinity') or {})
        hiring = fin.get('hiring_activity') or {}
        th = fin.get('topic_hiring') or {}
        outreach = OUTREACH.get(name, {})
        contacts = CONTACTS.get(name, [])

        pdf.add_page()

        # Company name header
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(41, 65, 122)
        pdf.cell(0, 10, safe(name))
        pdf.ln(8)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 6, safe(f'{co.get("industry", "")} | {co.get("address", "")}'))
        pdf.ln(10)
        pdf.set_text_color(0, 0, 0)

        # Overall Score big
        score = lead.get('overall_score') or 0
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(35, 8, 'Overall Score:')
        pdf.set_font('Helvetica', 'B', 18)
        if score >= 0.7:
            pdf.set_text_color(46, 139, 87)
        elif score >= 0.5:
            pdf.set_text_color(218, 165, 32)
        else:
            pdf.set_text_color(178, 34, 34)
        pdf.cell(20, 8, f'{score:.1%}')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', '', 9)
        cr = fin.get('customer_rating', 0) or 0
        pdf.cell(0, 8, f'    Customer Rating: {cr:.0%}')
        pdf.ln(12)

        # Stammdaten
        pdf.section('Stammdaten')
        pdf.kv('Website', co.get('website'))
        pdf.kv('Adresse', co.get('address'))
        pdf.kv('Branche', co.get('industry'))
        pdf.kv('Umsatz', fin.get('revenue_estimate'))
        pdf.kv('Mitarbeiter', fin.get('employee_count'))
        pdf.ln(3)

        # Scores
        pdf.section('Scoring')
        pdf.score_bar('Firmengesundheit', health.get('activity_score', 0) or 0)
        pdf.score_bar('Themen-Affinitaet', affinity.get('affinity_score', 0) or 0)
        pdf.score_bar('Size Fit', sf.get('size_fit_score', 0) or 0)
        pdf.score_bar('Marktdruck', sf.get('pressure_score', 0) or 0)
        pdf.score_bar('Hiring allg.', hiring.get('general_hiring_score', 0) or 0)
        pdf.score_bar('Topic Hiring', th.get('topic_hiring_score', 0) or 0)
        pdf.ln(3)

        # Key reasoning
        reasoning = sf.get('strategic_reasoning') or fin.get('rating_reasoning', '')
        if reasoning:
            pdf.section('Strategische Einschaetzung')
            pdf.set_font('Helvetica', '', 9)
            pdf.multi_cell(0, 5, safe(reasoning, 600))
            pdf.ln(3)

        # Ansprechpartner
        if contacts:
            pdf.section('Ansprechpartner')
            for c in contacts:
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(55, 6, safe(c['name']))
                pdf.set_font('Helvetica', '', 9)
                pdf.cell(80, 6, safe(c['role']))
                conf = c.get('conf', '')
                if conf == 'HIGH':
                    pdf.set_text_color(46, 139, 87)
                elif conf == 'MEDIUM':
                    pdf.set_text_color(218, 165, 32)
                else:
                    pdf.set_text_color(178, 34, 34)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(0, 6, conf)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(7)
            pdf.ln(3)

        # Outreach
        if outreach:
            pdf.section('Outreach-Vorlage')
            pdf.set_font('Helvetica', 'B', 9)
            pdf.cell(18, 6, 'Betreff:')
            pdf.set_font('Helvetica', 'I', 9)
            pdf.multi_cell(0, 6, safe(outreach.get('betreff', '')))
            pdf.ln(2)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.cell(22, 6, 'Aufhaenger:')
            pdf.set_font('Helvetica', '', 9)
            pdf.multi_cell(0, 5, safe(outreach.get('aufhaenger', ''), 400))
            pdf.ln(3)

    # Save
    out = 'iot_lead_sheets.pdf'
    pdf.output(out)
    print(f'PDF erstellt: {out} ({pdf.page_no()} Seiten)')


if __name__ == '__main__':
    main()
