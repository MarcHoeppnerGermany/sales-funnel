#!/usr/bin/env python3
"""Generate Excel workbook with all leads across all pipelines."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Style constants
HEADER_FONT = Font(name='Calibri', bold=True, color='FFFFFF', size=10)
HEADER_FILL = PatternFill(start_color='29417A', end_color='29417A', fill_type='solid')
TIER1_FILL = PatternFill(start_color='E8F5E9', end_color='E8F5E9', fill_type='solid')
TIER2_FILL = PatternFill(start_color='FFF8E1', end_color='FFF8E1', fill_type='solid')
TIER3_FILL = PatternFill(start_color='FFEBEE', end_color='FFEBEE', fill_type='solid')
SCORE_HIGH = Font(name='Calibri', bold=True, color='2E8B57', size=10)
SCORE_MED = Font(name='Calibri', bold=True, color='DAA520', size=10)
SCORE_LOW = Font(name='Calibri', bold=True, color='B22222', size=10)
THIN_BORDER = Border(
    left=Side(style='thin', color='D0D0D0'),
    right=Side(style='thin', color='D0D0D0'),
    top=Side(style='thin', color='D0D0D0'),
    bottom=Side(style='thin', color='D0D0D0'),
)
WRAP = Alignment(wrap_text=True, vertical='top')
WRAP_CENTER = Alignment(wrap_text=True, vertical='top', horizontal='center')

# Contact data from research
CONTACTS = {
    'Rosenberger Hochfrequenztechnik': 'Walter Hoelblinger, MBA | CIO (seit Jan 2025) | HIGH',
    'Mekra Lang GmbH': 'Michael Ammon | Global Head of IT | HIGH',
    'ACO Severin Ahlmann': 'Dominik Neff | CIO Group (seit Sep 2022, Ex-HELM AG) | HIGH',
    'GP JOULE GmbH': 'Kerrit Friedrichsen | CIO | HIGH',
    'Stern-Wywiol Gruppe': 'Kay Postwig | Head of IT/OT | HIGH',
    'Sikora AG': 'Christoph Hueniken | IT-Leiter | HIGH',
    'Nordex SE': 'Stefan Ewald | CIO, Head of IT & Org | HIGH',
    'SH Netz AG (HanseWerk)': 'Thorsten Frye | CIO & CDO | HIGH\nLisa Hebenstreit | GF Netztechnik | HIGH',
    'Harburg-Freudenberger Maschinenbau (HF Group)': 'Alexander Bodi | Head of IT (71 MA) | HIGH',
    'Fritz Winter Eisengiesserei': 'Alexander Schwab | Leiter IT & Digitalisierung | HIGH',
    'Klosterfrau Healthcare Group': 'Frank Roth | CIO (seit 2002) | HIGH',
    'GoodMills Deutschland GmbH': 'Daniel Wellenreuther | IT Business Dev Mgr | MEDIUM',
    'Gentherm Praezision SE': 'Ramzi Braham | VP & CIO (global, USA) | MEDIUM',
    'FFG Flensburger Fahrzeugbau': 'Stefan Koesterke | CISO | MEDIUM',
    'Helbako GmbH': 'Martin Niermann | Leiter Logistik/IT | MEDIUM',
    'Brunsbuettel Ports GmbH': 'Frank Schnabel | GF (Digitalprojekte) | MEDIUM',
    'Helm AG': 'Thomas Roos | CIO (verifizieren) | MEDIUM',
    'Limtronik': 'Gerd Ohl | GF / I4.0-Treiber | MEDIUM',
    'Blohm+Voss': 'Sebastian Herke | Senior IT/Data (NVL) | MEDIUM',
    'H. & J. Brueggen KG': 'Joachim Klamroth | CIO (seit 2021, Status pruefen) | MEDIUM',
    'Sweet Tec GmbH': 'Ralf Schulzke | kfm. GF (SAP-Entscheider) | MEDIUM',
    'SHW Automotive GmbH': 'Klaus Saiger | SAP Prozessmanager (Einstieg) | MEDIUM',
    'SAACKE GmbH': 'VAKANT (Kammer zu Rheinmetall) | MEDIUM',
    'Alfred PRACHT Lichttechnik': 'Gerhard Hillebrand | IoT-Engineer | MEDIUM',
    'Tamsen Maritim GmbH': 'Gregor Uloth | Techn. Betriebsleiter | MEDIUM',
    'Heinrich Roenner Gruppe': 'Roenner Verwaltungs-GmbH (IT-Hub) | LOW',
    'TROX SE': 'Thomas Mosbacher | Vorstand (IT-Ressort) | MEDIUM\nMatthias Schenk | Head of IT X-Fans | MEDIUM',
    'MRS Electronic GmbH': 'SONDERSITUATION: Wuerth-Uebernahme Maerz 2026',
    'Denker & Wulf AG': 'nicht gefunden | LOW',
    'CODAN Medizintechnik': 'nicht gefunden (3 IT-Stellen offen) | LOW',
    'Friesenkrone Feinkost': 'nicht gefunden | LOW',
}

# Tier assignments
TIER1 = [
    'Rosenberger Hochfrequenztechnik', 'Mekra Lang GmbH', 'ACO Severin Ahlmann',
    'GP JOULE GmbH', 'Stern-Wywiol Gruppe', 'Sikora AG', 'Nordex SE',
    'SH Netz AG (HanseWerk)', 'Harburg-Freudenberger Maschinenbau (HF Group)',
    'Fritz Winter Eisengiesserei', 'Klosterfrau Healthcare Group',
]
TIER2 = [
    'GoodMills Deutschland GmbH', 'Gentherm Praezision SE', 'TROX SE',
    'FFG Flensburger Fahrzeugbau', 'H. & J. Brueggen KG', 'Helbako GmbH',
    'Brunsbuettel Ports GmbH', 'Helm AG', 'SHW Automotive GmbH',
    'SAACKE GmbH', 'Tamsen Maritim GmbH', 'Sweet Tec GmbH',
    'Alfred PRACHT Lichttechnik', 'Limtronik', 'Heinrich Roenner Gruppe',
    'Blohm+Voss',
]

# Outreach subjects
OUTREACH_SUBJECTS = {
    'Rosenberger Hochfrequenztechnik': 'Vom CISO zum CIO bei Rosenberger - wie weit ist der IoT-Kern?',
    'Mekra Lang GmbH': 'Kamerasysteme, Digital-Business-Thesis und IoT - passt das zusammen?',
    'ACO Severin Ahlmann': 'Von HELM zu ACO: Smart Drainage als naechster IoT-Move?',
    'GP JOULE GmbH': 'Wind + PV + H2 unter einem Asset-Dach - wie, Herr Friedrichsen?',
    'Stern-Wywiol Gruppe': 'IT/OT in einer Rolle + 12 Firmen: Wo ist der gemeinsame Asset-Kern?',
    'Sikora AG': 'Sikoras Sensorik trifft Asset-IoT - Austausch auf Augenhoehe?',
    'Nordex SE': '6.800 Turbinen + Acciona-SAP: die Nische neben Mindtree?',
    'SH Netz AG (HanseWerk)': '24 Jahre HanseWerk Natur - Gespraech zur LoRaWAN-Asset-Bruecke?',
    'Harburg-Freudenberger Maschinenbau (HF Group)': 'ECM steht - wie nah ist HF Mixing an einer Asset-Schicht?',
    'Fritz Winter Eisengiesserei': 'Nach 75% IT-Leerlauf: Was macht der Asset-Kern jetzt?',
    'Klosterfrau Healthcare Group': '2002-heute: Aehnliche Langstrecke - Asset-IoT fuer Berlin/Luechow?',
}


def score_font(val):
    if val >= 0.7:
        return SCORE_HIGH
    elif val >= 0.5:
        return SCORE_MED
    return SCORE_LOW


def pct(val):
    if val is None:
        return ''
    return f'{val:.0%}'


def safe(text):
    if not text:
        return ''
    t = str(text)
    t = t.replace('–', '-').replace('—', '-')
    t = t.replace('‘', "'").replace('’', "'")
    t = t.replace('“', '"').replace('”', '"')
    t = t.replace('…', '...').replace(' ', ' ')
    t = t.replace('→', '->').replace('²', '2')
    return t


def style_header(ws, row, cols):
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = WRAP_CENTER
        cell.border = THIN_BORDER


def auto_width(ws, min_w=8, max_w=40):
    for col_cells in ws.columns:
        lengths = []
        for cell in col_cells:
            if cell.value:
                lines = str(cell.value).split('\n')
                lengths.append(max(len(l) for l in lines))
        if lengths:
            w = min(max(max(lengths) + 2, min_w), max_w)
            ws.column_dimensions[get_column_letter(col_cells[0].column)].width = w


def get_tier(name):
    # Normalize for matching
    for n in TIER1:
        if n in name or name in n:
            return 'TIER 1 HOT'
    for n in TIER2:
        if n in name or name in n:
            return 'TIER 2 WARM'
    if 'MRS Electronic' in name:
        return 'SONDER (M&A)'
    return 'TIER 3 COLD'


def get_contact(name):
    for k, v in CONTACTS.items():
        if k in name or name in k:
            return v
    return ''


def get_outreach(name):
    for k, v in OUTREACH_SUBJECTS.items():
        if k in name or name in k:
            return v
    return ''


def classify_pipeline(lead, idx, total_iot):
    """Determine which pipeline a lead belongs to."""
    ind = (lead['company'].get('industry') or '').lower()
    name = lead['company'].get('name', '')
    if 'fernwaerme' in ind or 'waermeversorgung' in ind or 'kommunale energie' in ind or 'contracting' in ind:
        return 'Fernwaerme'
    if any(x in ind.lower() for x in ['energiehandel', 'mineraloel', 'raffinerie', 'tanklager', 'bunker', 'rohstoff', 'stahl']):
        return 'Energiehandel'
    return 'IoT'


def main():
    with open('leads.json') as f:
        data = json.load(f)

    wb = Workbook()

    # ============ SHEET 1: Alle Leads Uebersicht ============
    ws = wb.active
    ws.title = 'Alle Leads'
    headers = [
        'Nr', 'Pipeline', 'Tier', 'Firma', 'Branche', 'Standort', 'Website',
        'Umsatz', 'Mitarbeiter', 'Overall Score', 'Customer Rating',
        'Gesundheit', 'Affinitaet', 'Size Fit', 'Marktdruck',
        'Hiring', 'Topic Hiring', 'Ansprechpartner', 'Outreach-Betreff',
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for i, lead in enumerate(sorted(data['leads'], key=lambda x: -(x.get('overall_score') or 0))):
        co = lead['company']
        name = co.get('name', '')
        tr = lead.get('topic_relevance') or {}
        fin = lead.get('financials') or {}
        sf = fin.get('strategic_fit') or {}
        health = (tr.get('company_health') or {})
        affinity = (tr.get('topic_affinity') or {})
        hiring = fin.get('hiring_activity') or {}
        th = fin.get('topic_hiring') or {}
        score = lead.get('overall_score') or 0
        cr = fin.get('customer_rating', 0) or 0
        pipeline = classify_pipeline(lead, i, 0)
        tier = get_tier(name)
        contact = get_contact(name)
        outreach = get_outreach(name)

        values = [
            row - 1, pipeline, tier, safe(name),
            safe(co.get('industry')), safe(co.get('address')), safe(co.get('website')),
            safe(fin.get('revenue_estimate')), fin.get('employee_count') or '',
            score, cr,
            health.get('activity_score') or '', affinity.get('affinity_score') or '',
            sf.get('size_fit_score') or '', sf.get('pressure_score') or '',
            hiring.get('general_hiring_score') or '', th.get('topic_hiring_score') or '',
            safe(contact), safe(outreach),
        ]
        for col, val in enumerate(values, 1):
            cell = ws.cell(row=row, column=col, value=val)
            cell.alignment = WRAP
            cell.border = THIN_BORDER
            # Score formatting
            if col in (10, 11) and isinstance(val, (int, float)) and val > 0:
                cell.number_format = '0%'
                cell.font = score_font(val)
            elif col in range(12, 18) and isinstance(val, (int, float)) and val > 0:
                cell.number_format = '0%'

        # Tier color
        if 'TIER 1' in tier:
            fill = TIER1_FILL
        elif 'TIER 2' in tier:
            fill = TIER2_FILL
        else:
            fill = TIER3_FILL
        for col in range(1, len(headers) + 1):
            ws.cell(row=row, column=col).fill = fill

        row += 1

    ws.auto_filter.ref = f'A1:{get_column_letter(len(headers))}{row - 1}'
    ws.freeze_panes = 'A2'
    auto_width(ws)

    # ============ SHEET 2: IoT TIER 1 Detail ============
    ws2 = wb.create_sheet('IoT TIER 1 Detail')
    h2 = ['Nr', 'Firma', 'Score', 'Ansprechpartner', 'Rolle', 'Konfidenz',
           'Betreff-Vorlage', 'Aufhaenger', 'Strategische Einschaetzung']
    for col, h in enumerate(h2, 1):
        ws2.cell(row=1, column=col, value=h)
    style_header(ws2, 1, len(h2))

    tier1_leads = []
    for lead in data['leads']:
        name = lead['company']['name']
        for t1 in TIER1:
            if t1 in name or name in t1:
                tier1_leads.append(lead)
                break
    tier1_leads.sort(key=lambda x: -(x.get('overall_score') or 0))

    AUFHAENGER = {
        'Rosenberger Hochfrequenztechnik': 'CISO->CIO Wechsel, "IT als Business Enabler", CISSP + MBA',
        'Mekra Lang GmbH': 'Studiert Master Digital Business neben dem Job. MEKRA View = IoT-Produkt.',
        'ACO Severin Ahlmann': 'Ex-HELM AG (2012-2019). Entwaesserungstechnik = verteilte Infrastruktur.',
        'GP JOULE GmbH': 'Neuer CIO. Wind+PV+H2+E-Mobility = heterogenstes Asset-Portfolio.',
        'Stern-Wywiol Gruppe': 'Seltene IT/OT-Doppelrolle. SternConnect Digi-Unit. 12 Spezialfirmen.',
        'Sikora AG': 'Sikora ist selbst Sensorhersteller. Sparring auf Augenhoehe.',
        'Nordex SE': 'Cumulocity SCADA, 6.800+ Turbinen, Mindtree-5J-Deal, Acciona-Integration.',
        'SH Netz AG (HanseWerk)': '24 Jahre HanseWerk Natur! LoRaWAN 60->400 Antennen. Bridge Strom/Waerme.',
        'Harburg-Freudenberger Maschinenbau (HF Group)': '71 MA IT, ECM mit ACTIWARE/ELO, 4 Business Units.',
        'Fritz Winter Eisengiesserei': 'CIO.de-Feature Feb 2026 "75% IT-Leerlauf". NetApp uSCALE. SAP fertig.',
        'Klosterfrau Healthcare Group': 'CIO seit 2002 (24 Jahre wie wir!). S/4HANA seit 2021. Picavi Smart Glasses.',
    }

    row = 2
    for i, lead in enumerate(tier1_leads, 1):
        name = lead['company']['name']
        fin = lead.get('financials') or {}
        sf = fin.get('strategic_fit') or {}
        contact_str = get_contact(name)
        # Split contact into name/role/conf
        parts = contact_str.split('|') if '|' in contact_str else [contact_str, '', '']
        c_name = parts[0].strip() if len(parts) > 0 else ''
        c_role = parts[1].strip() if len(parts) > 1 else ''
        c_conf = parts[2].strip() if len(parts) > 2 else ''

        aufh = ''
        for k, v in AUFHAENGER.items():
            if k in name or name in k:
                aufh = v
                break

        outreach = get_outreach(name)
        reasoning = safe(sf.get('strategic_reasoning') or fin.get('rating_reasoning', ''))

        values = [i, safe(name), lead.get('overall_score') or 0,
                  safe(c_name), safe(c_role), safe(c_conf),
                  safe(outreach), safe(aufh), reasoning]
        for col, val in enumerate(values, 1):
            cell = ws2.cell(row=row, column=col, value=val)
            cell.alignment = WRAP
            cell.border = THIN_BORDER
            cell.fill = TIER1_FILL
            if col == 3 and isinstance(val, (int, float)):
                cell.number_format = '0%'
                cell.font = score_font(val)
        row += 1

    auto_width(ws2, max_w=50)
    ws2.freeze_panes = 'A2'

    # ============ SHEET 3: Scoring Detail ============
    ws3 = wb.create_sheet('Scoring Detail')
    h3 = ['Firma', 'Pipeline', 'Overall', 'Gesundheit', 'Gesundheit Text',
           'Affinitaet', 'Affinitaet Text', 'Size Fit', 'Marktdruck',
           'Financial Health', 'Hiring', 'Topic Hiring', 'Topic Hiring Text',
           'Strategische Bewertung']
    for col, h in enumerate(h3, 1):
        ws3.cell(row=1, column=col, value=h)
    style_header(ws3, 1, len(h3))

    row = 2
    for lead in sorted(data['leads'], key=lambda x: -(x.get('overall_score') or 0)):
        co = lead['company']
        tr = lead.get('topic_relevance') or {}
        fin = lead.get('financials') or {}
        sf = fin.get('strategic_fit') or {}
        health = tr.get('company_health') or {}
        affinity = tr.get('topic_affinity') or {}
        hiring = fin.get('hiring_activity') or {}
        th = fin.get('topic_hiring') or {}
        pipeline = classify_pipeline(lead, 0, 0)

        values = [
            safe(co.get('name')), pipeline,
            lead.get('overall_score') or '',
            health.get('activity_score') or '',
            safe(health.get('activity_reasoning', '')),
            affinity.get('affinity_score') or '',
            safe(affinity.get('affinity_reasoning', '')),
            sf.get('size_fit_score') or '',
            sf.get('pressure_score') or '',
            sf.get('financial_health_score') or '',
            hiring.get('general_hiring_score') or '',
            th.get('topic_hiring_score') or '',
            safe(th.get('topic_hiring_reasoning', '')),
            safe(sf.get('strategic_reasoning', '')),
        ]
        for col, val in enumerate(values, 1):
            cell = ws3.cell(row=row, column=col, value=val)
            cell.alignment = WRAP
            cell.border = THIN_BORDER
            if col in (3, 4, 6, 8, 9, 10, 11, 12) and isinstance(val, (int, float)) and val > 0:
                cell.number_format = '0%'
        row += 1

    ws3.auto_filter.ref = f'A1:{get_column_letter(len(h3))}{row - 1}'
    ws3.freeze_panes = 'A2'
    auto_width(ws3, max_w=60)

    out = 'iot_leads_komplett.xlsx'
    wb.save(out)
    print(f'Excel erstellt: {out} ({row - 2} Leads, 3 Sheets)')


if __name__ == '__main__':
    main()
