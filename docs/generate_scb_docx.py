#!/usr/bin/env python3
"""
Generates a professional sales reference document (DOCX) for the
IoT/Telematics platform project (anonymized).

Uses NeoGeo New Media GmbH Corporate Design System:
  - NeoGeo Orange (#E67E22), Gold (#FFA500), Black (#0A0A0A)
  - Segoe UI / Arial typography
  - NeoGeo logo in header

Usage:
    python docs/generate_scb_docx.py

Output:
    docs/scb_telematics_referenz.docx
"""

import os
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# NeoGeo Brand Colors (from SKILL.md)
# ---------------------------------------------------------------------------
NG_ORANGE = RGBColor(0xE6, 0x7E, 0x22)
NG_GOLD = RGBColor(0xFF, 0xA5, 0x00)
NG_BLACK = RGBColor(0x0A, 0x0A, 0x0A)
NG_BRONZE = RGBColor(0xB8, 0x86, 0x0B)
NG_BLUE = RGBColor(0x4A, 0x90, 0xD9)
NG_GREEN = RGBColor(0x5C, 0xB8, 0x5C)
NG_CHARCOAL = RGBColor(0x21, 0x21, 0x21)
NG_DARK_GRAY = RGBColor(0x42, 0x42, 0x42)
NG_MID_GRAY = RGBColor(0x75, 0x75, 0x75)
NG_LIGHT_GRAY = RGBColor(0xE0, 0xE0, 0xE0)
NG_OFF_WHITE = RGBColor(0xF5, 0xF5, 0xF5)
NG_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# Logo paths
LOGO_PATH = BASE / "neogeo_logo.png"
LOGO_SMALL_PATH = BASE / "neogeo_logo_small.png"


# ---------------------------------------------------------------------------
# Helper functions — NeoGeo Style
# ---------------------------------------------------------------------------

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def remove_table_borders(tbl):
    tbl_element = tbl._tbl
    tblPr = tbl_element.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_orange_line(doc, width=Cm(7)):
    """Orange accent line (NeoGeo brand element)."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    cell.width = width
    cell.text = ""
    row = tbl.rows[0]
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trHeight = parse_xml(f'<w:trHeight {nsdecls("w")} w:val="50" w:hRule="exact"/>')
    trPr.append(trHeight)
    set_cell_shading(cell, "E67E22")
    remove_table_borders(tbl)


def add_gray_line(doc):
    """Thin gray separator line."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    cell.text = ""
    row = tbl.rows[0]
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trHeight = parse_xml(f'<w:trHeight {nsdecls("w")} w:val="15" w:hRule="exact"/>')
    trPr.append(trHeight)
    set_cell_shading(cell, "E0E0E0")
    remove_table_borders(tbl)


def add_section_title(doc, text):
    """H1: Charcoal #212121, 18pt Bold, orange underline."""
    p = doc.add_paragraph()
    p.space_before = Pt(18)
    p.space_after = Pt(2)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = NG_CHARCOAL
    run.font.name = "Segoe UI"
    add_orange_line(doc)


def add_sub_title(doc, text):
    """H2: Orange #E67E22, 14pt Semibold."""
    p = doc.add_paragraph()
    p.space_before = Pt(12)
    p.space_after = Pt(3)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = NG_ORANGE
    run.font.name = "Segoe UI"


def add_h3(doc, text):
    """H3: Dark Gray #424242, 12pt Semibold."""
    p = doc.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(2)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = NG_DARK_GRAY
    run.font.name = "Segoe UI"


def add_body_text(doc, text):
    """Body: Dark Gray #424242, 11pt."""
    p = doc.add_paragraph()
    p.space_after = Pt(6)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = NG_DARK_GRAY
    run.font.name = "Segoe UI"


def add_bullet(doc, text):
    """Bullet point in body style."""
    p = doc.add_paragraph(style="List Bullet")
    p.space_after = Pt(2)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = NG_DARK_GRAY
    run.font.name = "Segoe UI"


def add_key_value(doc, key, value):
    """Key-value: Bold charcoal key, regular dark gray value."""
    p = doc.add_paragraph()
    p.space_after = Pt(1)
    run_key = p.add_run(f"{key}: ")
    run_key.bold = True
    run_key.font.size = Pt(11)
    run_key.font.color.rgb = NG_CHARCOAL
    run_key.font.name = "Segoe UI"
    run_val = p.add_run(value)
    run_val.font.size = Pt(11)
    run_val.font.color.rgb = NG_DARK_GRAY
    run_val.font.name = "Segoe UI"


def add_highlight_box(doc, text):
    """Callout box with orange left border (NeoGeo style)."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    # Orange left border, light background
    set_cell_shading(cell, "FEF5ED")  # Orange @ ~8%
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="E67E22"/>'
        f'  <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    remove_table_borders(tbl)
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = NG_DARK_GRAY
    run.font.name = "Segoe UI"


def add_info_box(doc, text):
    """Info callout box with blue left border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "EDF4FC")  # Blue @ ~8%
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="4A90D9"/>'
        f'  <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    remove_table_borders(tbl)
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = NG_DARK_GRAY
    run.font.name = "Segoe UI"


def add_image_centered(doc, path, width=Cm(15)):
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(path), width=width)


def add_page_break(doc):
    doc.add_page_break()


# ---------------------------------------------------------------------------
# Build the DOCX — Anonymized, NeoGeo CI
# ---------------------------------------------------------------------------

def build_docx(chart_arch):
    doc = Document()

    # ---- Page margins (A4 per brand guide) ----
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # ---- Header: Logo left, title right ----
    header = doc.sections[0].header
    hp = header.paragraphs[0]
    if os.path.exists(LOGO_SMALL_PATH):
        run_logo = hp.add_run()
        run_logo.add_picture(str(LOGO_SMALL_PATH), height=Cm(1.5))
    hp.add_run("\t\t")
    run_title = hp.add_run("Projektreferenz: IoT-Telematik-Plattform")
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = NG_MID_GRAY
    run_title.font.name = "Segoe UI"

    # ---- Footer ----
    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run("NeoGeo New Media GmbH | Projektreferenz | M\u00e4rz 2026")
    run.font.size = Pt(9)
    run.font.color.rgb = NG_MID_GRAY
    run.font.name = "Segoe UI"

    # ================================================================
    # COVER PAGE
    # ================================================================
    doc.add_paragraph()

    # Logo centered
    if os.path.exists(LOGO_PATH):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(LOGO_PATH), width=Cm(4))

    doc.add_paragraph()

    # Double orange line
    add_orange_line(doc, Cm(16))
    p_spacer = doc.add_paragraph()
    p_spacer.space_before = Pt(2)
    p_spacer.space_after = Pt(2)
    add_orange_line(doc, Cm(16))

    doc.add_paragraph()

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Projektreferenz")
    run.bold = True
    run.font.size = Pt(28)
    run.font.color.rgb = NG_CHARCOAL
    run.font.name = "Segoe UI"

    # Subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Cloud-native IoT-Telematik-Plattform")
    run.font.size = Pt(16)
    run.font.color.rgb = NG_ORANGE
    run.font.name = "Segoe UI"

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("f\u00fcr einen f\u00fchrenden europ\u00e4ischen Trailer-Hersteller")
    run.font.size = Pt(16)
    run.font.color.rgb = NG_ORANGE
    run.font.name = "Segoe UI"

    doc.add_paragraph()

    # Gray separator
    add_gray_line(doc)

    doc.add_paragraph()

    # Metadata
    meta = [
        ("Branche", "Nutzfahrzeuge / Trailer-Herstellung"),
        ("Plattform", "IoT-Telematik mit Cloud-Backend"),
        ("Zertifizierung", "TISAX Stufe 3 (AL 3) \u2014 h\u00f6chste Sicherheitsstufe"),
        ("Auszeichnung", "Cloud Native Rockstars Award 2022 (Kat. Digital Business)"),
        ("Datum", "M\u00e4rz 2026"),
    ]
    for k, v in meta:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rk = p.add_run(f"{k}: ")
        rk.bold = True
        rk.font.size = Pt(11)
        rk.font.color.rgb = NG_MID_GRAY
        rk.font.name = "Segoe UI"
        rv = p.add_run(v)
        rv.font.size = Pt(11)
        rv.font.color.rgb = NG_MID_GRAY
        rv.font.name = "Segoe UI"

    # Company address at bottom
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for line in ["NeoGeo New Media GmbH", "Friedenstra\u00dfe 39", "25335 Elmshorn", "www.neogeo.com"]:
        run = p.add_run(line + "\n")
        run.font.size = Pt(9)
        run.font.color.rgb = NG_MID_GRAY
        run.font.name = "Segoe UI"

    # ================================================================
    # PAGE 2: Wer wir sind + Projekt\u00fcbersicht
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "1. Wer wir sind")

    add_body_text(
        doc,
        "NeoGeo New Media GmbH ist ein deutsches Software-Engineering-Team mit \u00fcber "
        "30 Jahren Erfahrung in der Entwicklung anspruchsvoller Softwaresysteme. Wir "
        "arbeiten seit Jahrzehnten mit namhaften Kunden aus Industrie, Logistik und "
        "Technologie \u2014 mit einem nachweislichen Track Record bei der Umsetzung "
        "komplexer Plattformprojekte."
    )

    add_highlight_box(
        doc,
        "TISAX Stufe 3 (AL 3) zertifiziert \u2014 h\u00f6chste Sicherheitsstufe f\u00fcr "
        "Informationssicherheit in der Automobilindustrie. Wir erf\u00fcllen die strengsten "
        "Anforderungen an Datenschutz, IT-Sicherheit und Vertraulichkeit."
    )

    add_sub_title(doc, "Skalierbar und kosteneffizient")

    add_body_text(
        doc,
        "\u00dcber unser etabliertes Nearshoring-Modell k\u00f6nnen wir Projektteams flexibel "
        "und kontrolliert skalieren \u2014 im europ\u00e4ischen Ausland und dar\u00fcber hinaus."
    )

    for b in [
        "Engineering und Steuerung in Deutschland \u2014 Architektur, Qualit\u00e4tssicherung, Projektleitung",
        "Kontrollierte Skalierung \u00fcber Nearshoring \u2014 erprobte Teams in Europa",
        "Kosten im Griff \u2014 Enterprise-Qualit\u00e4t ohne Enterprise-Preise",
        "Kein Kontrollverlust \u2014 durchg\u00e4ngige deutsche Projektverantwortung",
    ]:
        add_bullet(doc, b)

    # ================================================================
    # PAGE 3: Projekt\u00fcbersicht
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "2. Projekt\u00fcbersicht")

    add_body_text(
        doc,
        "Wir haben f\u00fcr einen der gr\u00f6\u00dften europ\u00e4ischen Trailer-Hersteller "
        "die komplette IoT-Telematik-Plattform entwickelt und betrieben \u2014 als alleiniger "
        "Entwicklungspartner. Architektur, Implementierung und Betrieb lagen zu 100% bei uns, "
        "nat\u00fcrlich in enger Abstimmung mit dem Kunden. Die Plattform vernetzt Trailer "
        "europaweit und bildet das R\u00fcckgrat seiner Digitalisierungsstrategie."
    )

    add_highlight_box(
        doc,
        "Auszeichnung: Cloud Native Rockstars Award 2022 (Kategorie Digital Business) \u2014 "
        "pr\u00e4sentiert auf der Cloud Native Conference in Garching bei M\u00fcnchen. "
        "Vortrag: \u201eNeue Telematik-Plattform in Rekordzeit entwickelt\u201c"
    )

    add_sub_title(doc, "Der Kunde")

    kv_data = [
        ("Branche", "Nutzfahrzeugbau / Trailer-Herstellung"),
        ("Position", "Europ\u00e4ischer Marktf\u00fchrer im Segment Sattelauflieger"),
        ("Gr\u00f6\u00dfe", "Mehrere tausend Mitarbeiter, Werke in \u00fcber 5 L\u00e4ndern"),
        ("Umsatz", "Mehrere Milliarden EUR Jahresumsatz"),
        ("Strategie", "Digitalisierung der gesamten Trailer-Flotte als Kernstrategie"),
    ]
    for k, v in kv_data:
        add_key_value(doc, k, v)

    add_info_box(
        doc,
        "Der Kunde wurde mehrfach f\u00fcr Digitalisierung und Innovation ausgezeichnet, "
        "u.a. als Digital Champion und TOP 100 Innovator."
    )

    # ================================================================
    # PAGE 4: Unsere Rolle & Leistungen
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "3. Unsere Rolle & Leistungen")

    add_body_text(
        doc,
        "NeoGeo war der alleinige Entwicklungspartner f\u00fcr die gesamte Plattform \u2014 "
        "von der Architektur \u00fcber die Implementierung bis zum laufenden Betrieb. "
        "Alle Entwicklungsschritte lagen zu 100% bei uns, in enger Abstimmung mit dem Kunden. "
        "Die Zusammenarbeit umfasst mehrere Jahre und ist durch den gemeinsam gewonnenen "
        "Cloud Native Rockstars Award 2022 \u00f6ffentlich dokumentiert."
    )

    add_sub_title(doc, "Projektziele")
    for b in [
        "Echtzeit-Tracking und -Monitoring aller Trailer-Parameter",
        "Herstellerunabh\u00e4ngige Sensorvernetzung \u00fcber alle Trailertypen",
        "Serienm\u00e4\u00dfige Telematik ab Werk als Industriestandard",
        "Sichere Daten\u00fcbertragung von der Stra\u00dfe in die Cloud",
        "Offene Datenplattform mit API f\u00fcr Drittanbieter-Integration",
        "Skalierung auf zehntausende Einheiten europaweit",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Unsere Leistungen")
    for b in [
        "Architektur und Entwicklung des Cloud-Backends (Microsoft Azure)",
        "Webportal f\u00fcr Flottenmanagement und Datenanalyse",
        "Mobile Apps f\u00fcr Disponenten und Fahrer",
        "API-Schnittstellen f\u00fcr TMS/ERP-Integration",
        "Bluetooth-basiertes Ladungstr\u00e4ger-Tracking",
        "Integration diverser Sensorik (Reifendruck, EBS, T\u00fcrstatus, Temperatur)",
    ]:
        add_bullet(doc, b)

    # ================================================================
    # PAGE 5: Technische Architektur
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "4. Technische Architektur")

    add_image_centered(doc, chart_arch, width=Cm(16))

    add_sub_title(doc, "Embedded / Edge")
    for b in [
        "Industrietaugliches Steuerger\u00e4t (IP6K9K) mit LTE und globalem Roaming",
        "Integrierter Akku f\u00fcr mehrere Monate Stand-by",
        "Bluetooth Low Energy f\u00fcr Nahbereichs-Tracking",
        "Anbindung diverser Sensorik \u00fcber Standardprotokolle",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Cloud-Plattform")
    for b in [
        "Microsoft Azure (IoT Hub, Event Hubs, Synapse Analytics, Data Explorer)",
        "Cloud-native Architektur mit horizontaler Skalierbarkeit",
        "Herstellerunabh\u00e4ngige Sensor-Anbindung",
        "Zero-Trust-Security-Konzept",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Datenplattform & Schnittstellen")
    for b in [
        "Data Management Center f\u00fcr kontrollierte Datenweitergabe an Partner",
        "REST-APIs f\u00fcr nahtlose TMS/ERP-Integration",
        "Anbindung f\u00fchrender Logistik-Plattformen",
        "Zertifizierter Temperaturrecorder (DIN EN 12830)",
    ]:
        add_bullet(doc, b)

    # ================================================================
    # PAGE 6: Ergebnisse & Business Impact
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "5. Ergebnisse & Business Impact")

    add_sub_title(doc, "Skalierung")
    for b in [
        "Zehntausende vernetzte Telematik-Einheiten europaweit im Einsatz",
        "Daten aus \u00fcber 20 europ\u00e4ischen L\u00e4ndern",
        "Eine der gr\u00f6\u00dften vernetzten Trailer-Flotten Europas",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Kundenmehrwert")
    for b in [
        "Echtzeit-Tracking: Position, Temperatur, Reifendruck, T\u00fcrstatus, EBS-Daten",
        "Predictive Maintenance: Vorausschauende Wartungsplanung",
        "Pr\u00e4zise Laufleistungsberechnung f\u00fcr optimierte Wartungsintervalle",
        "Reduzierter IT-Aufwand: Plug-and-Play ab Werk",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Strategische Wirkung")
    add_body_text(
        doc,
        "Die Plattform hat dem Kunden erm\u00f6glicht, ein \u00d6kosystem strategischer "
        "Partnerschaften mit f\u00fchrenden Logistik- und Flottenmanagement-Anbietern aufzubauen. "
        "Mehrere \u00f6ffentlich kommunizierte Kooperationen basieren auf der von uns "
        "mitentwickelten Datenplattform."
    )

    add_highlight_box(
        doc,
        "Die IoT-Plattform hat das Telematik-Angebot des Kunden zu einem der "
        "gr\u00f6\u00dften Trailer-Telematik-\u00d6kosysteme Europas gemacht und erm\u00f6glicht "
        "Partnerschaften mit f\u00fchrenden Akteuren der Logistik-Branche."
    )

    # ================================================================
    # PAGE 7: Technologie-Stack
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "6. Technologie-Stack")

    add_sub_title(doc, "Embedded / Hardware")
    for b in [
        "Industrietaugliches Steuerger\u00e4t mit LTE, WLAN, RFID",
        "Bluetooth Low Energy (Ladungstr\u00e4ger-Tracking)",
        "Standardprotokolle: LIN-Bus, 433-MHz, ABS/GPS",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Cloud & Backend")
    for b in [
        "Microsoft Azure (IoT Hub, Event Hubs, Synapse Analytics, Data Explorer)",
        "Herstellerunabh\u00e4ngige Sensor-Middleware",
        "Zero Trust Security",
        "SAP-Integration",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Frontend & Apps")
    for b in [
        "Webportal f\u00fcr Flottenmanagement und Datenanalyse",
        "Mobile App f\u00fcr Disponenten",
        "Mobile App f\u00fcr Fahrer",
        "Data Management Center",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Integration & Standards")
    for b in [
        "REST APIs f\u00fcr TMS/ERP-Systeme",
        "DIN EN 12830 (Temperaturrecorder)",
        "OPC-UA (Produktionssensorik)",
    ]:
        add_bullet(doc, b)

    add_sub_title(doc, "Zertifizierungen & Sicherheit")
    for b in [
        "TISAX Stufe 3 (AL 3) \u2014 h\u00f6chste Sicherheitsstufe Automobilindustrie",
        "Zero Trust Security Architecture",
        "DSGVO-konforme Datenverarbeitung",
    ]:
        add_bullet(doc, b)

    # ================================================================
    # PAGE 8: \u00dcber NeoGeo + Kontakt
    # ================================================================
    add_page_break(doc)
    add_section_title(doc, "7. \u00dcber NeoGeo New Media GmbH")

    add_body_text(
        doc,
        "NeoGeo New Media GmbH ist ein deutsches Software-Engineering-Unternehmen mit Sitz "
        "in Elmshorn und \u00fcber 30 Jahren Erfahrung. Wir sind spezialisiert auf die "
        "Entwicklung von IoT-Plattformen, Cloud-native Architekturen und datengetriebenen "
        "Applikationen f\u00fcr die Industrie und Logistik."
    )

    add_body_text(
        doc,
        "Wir sind TISAX Stufe 3 (AL 3) zertifiziert \u2014 die h\u00f6chste Sicherheitsstufe "
        "f\u00fcr Informationssicherheit in der Automobilindustrie. \u00dcber unser Nearshoring-Modell "
        "skalieren wir schnell und kosteneffizient: Engineering in Deutschland, kontrollierte "
        "Skalierung im europ\u00e4ischen Ausland und dar\u00fcber hinaus."
    )

    add_sub_title(doc, "Unsere Kernkompetenzen")
    for b in [
        "IoT-Plattformen und Telematik-Systeme",
        "Cloud-native Architekturen (Microsoft Azure)",
        "Embedded Software und Edge Computing",
        "Datenplattformen und Analytics",
        "Mobile und Web-Applikationen",
        "TMS/ERP-Integration",
    ]:
        add_bullet(doc, b)

    add_section_title(doc, "8. Kontakt")

    add_body_text(
        doc,
        "Wir freuen uns, Ihnen unser Leistungsspektrum im Detail vorzustellen."
    )
    add_body_text(
        doc,
        "Kontaktieren Sie uns f\u00fcr ein unverbindliches Gespr\u00e4ch \u00fcber Ihre "
        "IoT- und Telematik-Anforderungen."
    )

    # Contact details
    doc.add_paragraph()
    contact = [
        "NeoGeo New Media GmbH",
        "Friedenstra\u00dfe 39",
        "25335 Elmshorn",
        "www.neogeo.com",
    ]
    for line in contact:
        p = doc.add_paragraph()
        p.space_after = Pt(0)
        run = p.add_run(line)
        run.bold = True if line.startswith("NeoGeo") else False
        run.font.size = Pt(11)
        run.font.color.rgb = NG_CHARCOAL
        run.font.name = "Segoe UI"

    # ================================================================
    # Quellenhinweise & Disclaimer
    # ================================================================
    doc.add_paragraph()
    add_gray_line(doc)

    add_h3(doc, "Quellenhinweise")

    sources = [
        "Cloud Native Rockstars Award 2022: datacenter-insider.de, cloudnativeconference.de (Juli 2022)",
        "Marktdaten Trailer-Industrie: \u00f6ffentliche Branchenberichte und Fachpresse",
    ]
    for s in sources:
        add_bullet(doc, s)

    # Disclaimer
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run(
        "Hinweis: Dieses Dokument beschreibt unsere Rolle als Entwicklungspartner auf Basis "
        "\u00f6ffentlich zug\u00e4nglicher Informationen. Es werden keine vertraulichen oder "
        "NDA-gesch\u00fctzten Informationen weitergegeben. Die Zusammenarbeit ist durch den "
        "Cloud Native Rockstars Award 2022 \u00f6ffentlich dokumentiert."
    )
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = NG_MID_GRAY
    run.font.name = "Segoe UI"

    # ---- Save ----
    out_path = BASE / "scb_telematics_referenz.docx"
    doc.save(str(out_path))
    return str(out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    chart_arch = str(BASE / "chart_architektur.png")

    if not os.path.exists(chart_arch):
        print("Generating architecture diagram...")
        import importlib.util
        spec = importlib.util.spec_from_file_location("assets", str(BASE / "generate_assets.py"))
        assets = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(assets)
        assets.create_architecture_diagram()
        print("Chart ready.")

    print("Generating DOCX...")
    out = build_docx(chart_arch)
    print(f"  -> {out}")
    print("Done!")


if __name__ == "__main__":
    main()
