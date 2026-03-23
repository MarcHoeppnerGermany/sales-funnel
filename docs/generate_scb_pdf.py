#!/usr/bin/env python3
"""
Generates a professional sales reference document (PDF) for the
Schmitz Cargobull TrailerConnect Telematics project.

Usage:
    python docs/generate_scb_pdf.py

Output:
    docs/scb_telematics_referenz.pdf
"""

import os
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from fpdf import FPDF

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Color palette (SCB-inspired)
# ---------------------------------------------------------------------------
SCB_BLUE = "#003366"
SCB_LIGHT_BLUE = "#0066AA"
SCB_ORANGE = "#E87722"
SCB_GRAY = "#58595B"
SCB_LIGHT_GRAY = "#D9D9D9"
SCB_WHITE = "#FFFFFF"

# ---------------------------------------------------------------------------
# 1. Generate charts with matplotlib
# ---------------------------------------------------------------------------

def create_market_share_chart():
    """European trailer market share pie chart."""
    fig, ax = plt.subplots(figsize=(5, 3.5))
    labels = ["Schmitz\nCargobull\n25%", "Krone\n~15%", "Kögel\n~8%", "Wielton\n~7%", "Sonstige\n~45%"]
    sizes = [25, 15, 8, 7, 45]
    colors = [SCB_ORANGE, "#4A90D9", "#7BC8A4", "#F5A623", SCB_LIGHT_GRAY]
    explode = (0.06, 0, 0, 0, 0)
    wedges, texts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        startangle=90, textprops={"fontsize": 8, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    ax.set_title("Europäischer Trailer-Markt — Marktanteile", fontsize=10, fontweight="bold", pad=12, color=SCB_BLUE)
    fig.tight_layout()
    path = BASE / "chart_marktanteil.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)
    return str(path)


def create_telematics_growth_chart():
    """TrailerConnect units over time."""
    fig, ax = plt.subplots(figsize=(5.5, 3))
    years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    units_sold = [15, 25, 35, 48, 60, 72, 85, 95]  # cumulative in thousands
    active = [10, 18, 26, 35, 44, 52, 58, 65]

    ax.bar([x for x in range(len(years))], units_sold, color=SCB_LIGHT_BLUE, alpha=0.85, label="Verkauft (kum.)", width=0.4, align="edge")
    ax.bar([x + 0.4 for x in range(len(years))], active, color=SCB_ORANGE, alpha=0.85, label="Aktiv", width=0.4, align="edge")
    ax.set_xticks([x + 0.4 for x in range(len(years))])
    ax.set_xticklabels(years, fontsize=8)
    ax.set_ylabel("Einheiten (Tsd.)", fontsize=8)
    ax.set_title("TrailerConnect® Telematik-Einheiten", fontsize=10, fontweight="bold", color=SCB_BLUE)
    ax.legend(fontsize=7, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 110)
    fig.tight_layout()
    path = BASE / "chart_telematik_wachstum.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)
    return str(path)


def create_architecture_diagram():
    """Simplified system architecture diagram."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    box_style = dict(boxstyle="round,pad=0.4", facecolor=SCB_LIGHT_BLUE, edgecolor=SCB_BLUE, alpha=0.9)
    box_orange = dict(boxstyle="round,pad=0.4", facecolor=SCB_ORANGE, edgecolor="#CC6600", alpha=0.9)
    box_gray = dict(boxstyle="round,pad=0.4", facecolor=SCB_LIGHT_GRAY, edgecolor=SCB_GRAY, alpha=0.9)
    text_kw = dict(fontsize=8, ha="center", va="center", fontweight="bold", color="white")
    text_dark = dict(fontsize=8, ha="center", va="center", fontweight="bold", color=SCB_BLUE)

    # Trailer layer
    ax.text(1.5, 5.2, "Trailer", fontsize=9, fontweight="bold", color=SCB_BLUE, ha="center")
    sensors = ["CTU\nSteuergerät", "TPMS\nSensoren", "EBS /\nABS", "Tür-\nsensorik", "Temp.-\nRecorder"]
    for i, s in enumerate(sensors):
        kw = {**text_kw, "fontsize": 6.5}
        ax.text(0.5 + i * 1.8, 4.3, s, bbox=box_style, **kw)

    # Connectivity
    ax.annotate("", xy=(5, 3.5), xytext=(5, 3.9), arrowprops=dict(arrowstyle="->", color=SCB_ORANGE, lw=2))
    ax.text(5, 3.7, "LTE / Global Roaming", fontsize=7, ha="center", color=SCB_ORANGE, fontstyle="italic")

    # Cloud layer
    ax.text(5, 3.1, "Microsoft Azure\nIoT Hub & Cloud", bbox=box_orange, **text_kw)

    # Services
    ax.annotate("", xy=(2, 2.0), xytext=(3.8, 2.6), arrowprops=dict(arrowstyle="->", color=SCB_GRAY, lw=1.5))
    ax.annotate("", xy=(5, 2.0), xytext=(5, 2.6), arrowprops=dict(arrowstyle="->", color=SCB_GRAY, lw=1.5))
    ax.annotate("", xy=(8, 2.0), xytext=(6.2, 2.6), arrowprops=dict(arrowstyle="->", color=SCB_GRAY, lw=1.5))

    kw_dark7 = {**text_dark, "fontsize": 7}
    ax.text(2, 1.5, "TrailerConnect®\nPortal", bbox=box_gray, **kw_dark7)
    ax.text(5, 1.5, "beUpToDate\nApp", bbox=box_gray, **kw_dark7)
    ax.text(8, 1.5, "Data Mgmt.\nCenter (API)", bbox=box_gray, **kw_dark7)

    # End users
    ax.text(2, 0.5, "Disponent", fontsize=7, ha="center", color=SCB_GRAY)
    ax.text(5, 0.5, "Fahrer", fontsize=7, ha="center", color=SCB_GRAY)
    ax.text(8, 0.5, "TMS / ERP\nIntegration", fontsize=7, ha="center", color=SCB_GRAY)

    ax.set_title("Systemarchitektur — TrailerConnect® Telematik", fontsize=10, fontweight="bold", color=SCB_BLUE, pad=8)
    fig.tight_layout()
    path = BASE / "chart_architektur.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)
    return str(path)


# ---------------------------------------------------------------------------
# 2. Build the PDF
# ---------------------------------------------------------------------------

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

class SCBDocument(FPDF):
    """Custom PDF with header/footer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf", uni=True)
        self.add_font("DejaVu", "I", f"{FONT_DIR}/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "BI", f"{FONT_DIR}/DejaVuSans-Bold.ttf", uni=True)

    def header(self):
        self.set_font("DejaVu", "B", 8)
        self.set_text_color(0, 51, 102)
        self.cell(0, 6, "Projektreferenz: Schmitz Cargobull TrailerConnect\u00ae Telematik", align="R")
        self.ln(8)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.4)
        self.line(10, 14, 200, 14)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 7)
        self.set_text_color(88, 89, 91)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}} — Erstellt: März 2026", align="C")

    def section_title(self, title):
        self.set_font("DejaVu", "B", 13)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(232, 119, 34)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(0, 102, 170)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("DejaVu", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("DejaVu", "", 9)
        self.set_text_color(50, 50, 50)
        x = self.get_x()
        self.cell(5, 5, chr(8226))
        self.multi_cell(0, 5, text)
        self.ln(1)

    def key_value(self, key, value):
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(0, 51, 102)
        self.cell(50, 5, key + ":")
        self.set_font("DejaVu", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, value)
        self.ln(1)

    def highlight_box(self, text):
        self.set_fill_color(240, 245, 250)
        self.set_draw_color(0, 102, 170)
        self.set_line_width(0.3)
        y_start = self.get_y()
        self.set_font("DejaVu", "I", 9)
        self.set_text_color(0, 51, 102)
        self.set_x(15)
        self.multi_cell(180, 5, text, border=1, fill=True)
        self.ln(3)


def build_pdf(chart_markt, chart_wachstum, chart_arch):
    pdf = SCBDocument()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ---- Cover Page ----
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("DejaVu", "B", 28)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "Projektreferenz", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(232, 119, 34)
    pdf.cell(0, 12, "Schmitz Cargobull", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "TrailerConnect\u00ae Telematik-Plattform", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(232, 119, 34)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    pdf.set_font("DejaVu", "", 12)
    pdf.set_text_color(88, 89, 91)
    pdf.cell(0, 8, "IoT-Plattform f\u00fcr Europas gr\u00f6\u00dfte vernetzte Trailer-Flotte", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "95.000+ Telematik-Einheiten \u2014 65.000 aktive Systeme", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(232, 119, 34)
    pdf.cell(0, 8, "\u2605 Cloud Native Rockstars Award 2022 \u2014 Kategorie Digital Business \u2605", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("DejaVu", "I", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, "M\u00e4rz 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # ---- Page 2: Kundenüberblick ----
    pdf.add_page()
    pdf.section_title("1. Der Kunde: Schmitz Cargobull AG")

    pdf.key_value("Gegr\u00fcndet", "1892 in Altenberge, M\u00fcnsterland")
    pdf.key_value("Hauptsitz", "Horstmar, Deutschland")
    pdf.key_value("Umsatz GJ 2024/25", "2,16 Mrd. EUR")
    pdf.key_value("Mitarbeiter", "ca. 6.400")
    pdf.key_value("Produktion GJ 2024/25", "42.353 Einheiten")
    pdf.key_value("Marktanteil Europa", "25% (Zentraleuropa: 31%)")
    pdf.key_value("Werke", "Deutschland, Litauen, Spanien, England, T\u00fcrkei, Rum\u00e4nien")
    pdf.key_value("Segmente", "Curtainsider, K\u00fchlfahrzeuge, Kipper, Trockenfrachtauflieger")

    pdf.ln(3)
    pdf.body_text(
        "Schmitz Cargobull ist der f\u00fchrende europ\u00e4ische Hersteller von Sattelaufliegern und "
        "Marktf\u00fchrer in allen Kernsegmenten. Das Unternehmen hat \u00fcber 73 Mio. EUR im GJ 2024/25 "
        "in Produktentwicklung, Digitalisierung und Nachhaltigkeit investiert."
    )

    if os.path.exists(chart_markt):
        pdf.image(chart_markt, x=30, w=150)
        pdf.ln(5)

    pdf.highlight_box(
        "Auszeichnungen (Auswahl): Trailer Innovation 2019 (SmartTrailer), Digital Champion 2021 & 2022, "
        "Digital Innovator 2022, TOP 100 Innovator, Deutscher Nachhaltigkeitspreis 2025, "
        "Cloud Native Rockstars Award 2022 (Kat. Digital Business \u2014 gemeinsam mit Entwicklungspartner)"
    )

    # ---- Page 3: Projekt ----
    pdf.add_page()
    pdf.section_title("2. Das Projekt: TrailerConnect\u00ae Telematik")

    pdf.body_text(
        "Wir haben die IoT- und Telematik-Plattform TrailerConnect\u00ae f\u00fcr Schmitz Cargobull "
        "vollst\u00e4ndig konzipiert, entwickelt und betrieben \u2014 von der Systemarchitektur \u00fcber "
        "die Implementierung bis zum laufenden Betrieb. Die Plattform verwandelt jeden Trailer "
        "in ein IoT-Ger\u00e4t und bildet das R\u00fcckgrat der Digitalisierungsstrategie von Europas "
        "gr\u00f6\u00dftem Trailer-Hersteller."
    )
    pdf.highlight_box(
        "Auszeichnung: Cloud Native Rockstars Award 2022 (Kategorie Digital Business) \u2014 "
        "gemeinsam mit Schmitz Cargobull auf der Cloud Native Conference in Garching pr\u00e4sentiert. "
        "Vortrag: \u201eNeue Telematik-Plattform in Rekordzeit entwickelt\u201c"
    )

    pdf.sub_title("Projektziele")
    pdf.bullet("Echtzeit-Tracking und -Monitoring aller Trailer-Parameter")
    pdf.bullet("Herstellerunabh\u00e4ngige Sensorvernetzung \u00fcber alle Trailertypen")
    pdf.bullet("Standardm\u00e4\u00dfige Telematik ab Werk (\u201e100% SMART\u201c-Strategie seit 2018)")
    pdf.bullet("Sichere Daten\u00fcbertragung von der Stra\u00dfe in die Cloud")
    pdf.bullet("Offene Datenplattform mit API f\u00fcr Drittanbieter-Integration")
    pdf.bullet("Skalierung auf 95.000+ Einheiten in ganz Europa")

    pdf.ln(3)
    pdf.sub_title("Projektumfang & Leistungen")
    pdf.bullet("Entwicklung der Embedded-Software f\u00fcr das CTU-Steuerger\u00e4t (IP6K9K, LTE, globalem Roaming)")
    pdf.bullet("Cloud-Backend auf Microsoft Azure (IoT Hub, Event Hubs, Azure Synapse, Data Explorer)")
    pdf.bullet("TrailerConnect\u00ae Webportal mit FleetTrack, FleetWatch und Data Management Center")
    pdf.bullet("Mobile Apps: beUpToDate (Disponenten) und beSmart (Fahrer)")
    pdf.bullet("API-Schnittstellen f\u00fcr TMS/ERP-Integration (AddSecure, Transporeon, Shippeo, Trimble u.a.)")
    pdf.bullet("Bluetooth-basiertes Ladungstr\u00e4ger-Tracking (erste OEM-L\u00f6sung am Markt)")
    pdf.bullet("Integration von TPMS, EBS, T\u00fcsensorik, Temperaturrecorder, RFID, Tanksensor")

    if os.path.exists(chart_wachstum):
        pdf.ln(3)
        pdf.image(chart_wachstum, x=25, w=160)
        pdf.ln(3)

    # ---- Page 4: Architektur ----
    pdf.add_page()
    pdf.section_title("3. Technische Architektur")

    if os.path.exists(chart_arch):
        pdf.image(chart_arch, x=15, w=180)
        pdf.ln(5)

    pdf.sub_title("Hardware: CTU-Steuerger\u00e4t")
    pdf.bullet("Schutzklasse IP6K9K \u2014 staub- und hochdruckwasserfest")
    pdf.bullet("LTE-Mobilfunk mit globalem Roaming (keine Mehrkosten)")
    pdf.bullet("Integrierter Akku \u2014 mehrere Monate Stand-by")
    pdf.bullet("Verdeckter Einbau \u2014 Schutz vor Manipulation")
    pdf.bullet("Getestet: 690.000 km, 22 L\u00e4nder, 1.500+ Grenz\u00fcbertritte")
    pdf.bullet("Integriert: Beschleunigungssensor, 433-MHz TPMS-Empf\u00e4nger, WLAN, ABS/GPS, RFID")

    pdf.sub_title("Cloud-Plattform")
    pdf.bullet("Microsoft Azure: IoT Hub, Event Hubs, Azure Synapse Analytics, Data Explorer")
    pdf.bullet("Cloud-First-Strategie \u2014 lokale Rechenzentren aufgel\u00f6st")
    pdf.bullet("SAP-to-Azure Migration: 28 Systeme in 3 Monaten, 20% Betriebskostensenkung")
    pdf.bullet("CloudRail.Box f\u00fcr herstellerunabh\u00e4ngige Sensoranbindung (12.000+ Sensordefinitionen)")
    pdf.bullet("One Single-Gateway \u2014 abgesicherte Daten\u00fcbermittlung aller Sensoren und Aktoren")

    pdf.sub_title("Datenplattform & Schnittstellen")
    pdf.bullet("TrailerConnect\u00ae Data Management Center (DMC) f\u00fcr kontrollierte Datenweitergabe")
    pdf.bullet("REST-APIs f\u00fcr nahtlose TMS/ERP-Integration")
    pdf.bullet("Partner-Integrationen: AddSecure, CO3, Mapon, Sick Mobilisis, Shippeo, Trimble, Transporeon, Webfleet, Cartrack")
    pdf.bullet("DIN EN 12830 zertifizierter Temperaturrecorder")

    # ---- Page 5: Ergebnisse ----
    pdf.add_page()
    pdf.section_title("4. Ergebnisse & Gesch\u00e4ftswert")

    pdf.sub_title("Skalierung")
    pdf.bullet("95.000+ verkaufte Telematik-Einheiten europaweit")
    pdf.bullet("65.000+ aktive Systeme auf Europas Stra\u00dfen")
    pdf.bullet("Daten aus 22+ europ\u00e4ischen L\u00e4ndern")
    pdf.bullet("Erster und einziger Trailer-OEM mit serienmäßiger Telematik auch in Nicht-Kühlfahrzeugen")

    pdf.sub_title("Kundenmehrwert")
    pdf.bullet("Echtzeit-Tracking: Position, Temperatur, Reifendruck, T\u00fcrstatus, EBS-Daten")
    pdf.bullet("Predictive Maintenance: Vorausschauende Wartungsplanung \u00fcber FleetWatch")
    pdf.bullet("Ladungstr\u00e4ger-Tracking via Bluetooth \u2014 Branchen-Erstl\u00f6sung")
    pdf.bullet("Laufleistungsberechnung \u00fcber ABS + GPS f\u00fcr pr\u00e4zise Wartungsintervalle")
    pdf.bullet("Reduzierter IT-Aufwand: Plug-and-Play ab Werk, keine Nachr\u00fcstung n\u00f6tig")

    pdf.sub_title("Strategische Partnerschaften (erm\u00f6glicht durch die Plattform)")
    pdf.bullet("Webfleet (Bridgestone) \u2014 Integrierte Trailer-Telematik (Nov 2024)")
    pdf.bullet("AddSecure \u2014 Europaweite strategische Partnerschaft (Okt 2025)")
    pdf.bullet("Cartrack (Karooooo) \u2014 Integrierte Flottentelematik (Feb 2026)")
    pdf.bullet("Atlantis Global System \u2014 Mehrheitsbeteiligung K\u00fchlketten-Telematik (Jun 2024)")
    pdf.bullet("Utility Trailer \u2014 Joint Venture Nordamerika (M\u00e4rz 2025)")
    pdf.bullet("Krone Telematics \u2014 Hersteller\u00fcbergreifender Datenaustausch")

    pdf.ln(3)
    pdf.highlight_box(
        "\u201eDie IoT-Plattform hat TrailerConnect\u00ae zum gr\u00f6\u00dften Trailer-Telematik-\u00d6kosystem "
        "Europas gemacht und erm\u00f6glicht Partnerschaften mit den f\u00fchrenden Akteuren der Logistik-Branche.\u201c"
    )

    # ---- Page 6: Technologie-Stack ----
    pdf.add_page()
    pdf.section_title("5. Technologie-Stack")

    pdf.sub_title("Embedded / Hardware")
    pdf.bullet("CTU-Steuerger\u00e4t mit LTE, WLAN, RFID, 433-MHz TPMS")
    pdf.bullet("LIN-Bus-Anbindung (T\u00fcrverschlusssystem)")
    pdf.bullet("Bluetooth Low Energy (Ladungstr\u00e4ger-Tracking)")
    pdf.bullet("Patente: EP3392084A1, EP3618469A1, US 10,046,811")

    pdf.sub_title("Cloud & Backend")
    pdf.bullet("Microsoft Azure (IoT Hub, Event Hubs, Synapse Analytics, Data Explorer)")
    pdf.bullet("CloudRail f\u00fcr herstellerunabh\u00e4ngige Sensor-Anbindung")
    pdf.bullet("Zscaler Zero Trust Security")
    pdf.bullet("SAP S/4HANA on Azure")

    pdf.sub_title("Frontend & Apps")
    pdf.bullet("TrailerConnect\u00ae Webportal (FleetTrack, FleetWatch, TyreManager)")
    pdf.bullet("beUpToDate App (Disponenten)")
    pdf.bullet("beSmart App (Fahrer)")
    pdf.bullet("TrailerConnect\u00ae Data Management Center")

    pdf.sub_title("Integration & Standards")
    pdf.bullet("REST APIs f\u00fcr TMS/ERP-Systeme")
    pdf.bullet("OPC-UA (Produktionssensorik)")
    pdf.bullet("DIN EN 12830 (Temperaturrecorder)")
    pdf.bullet("IO-Link (Industriesensorik)")

    pdf.ln(5)
    pdf.section_title("6. Kontakt")
    pdf.body_text(
        "Wir freuen uns, Ihnen unser Leistungsspektrum und die Erfahrungen aus dem "
        "Schmitz Cargobull-Projekt im Detail vorzustellen."
    )
    pdf.ln(2)
    pdf.body_text(
        "Kontaktieren Sie uns f\u00fcr ein unverbindliches Gespr\u00e4ch \u00fcber Ihre "
        "IoT- und Telematik-Anforderungen."
    )

    pdf.ln(5)
    pdf.section_title("7. Quellenhinweise")
    pdf.set_font("DejaVu", "", 7)
    pdf.set_text_color(80, 80, 80)
    sources = [
        "Cloud Native Rockstars Award 2022: datacenter-insider.de, cloudnativeconference.de (Juli 2022)",
        "SCB Geschäftsbericht GJ 2024/25: cargobull.com/presse",
        "TrailerConnect Produktseite: cargobull.com/de/services/data-services",
        "SCB Partnerschaften: Pressemitteilungen auf cargobull.com (2024\u20132026)",
        "Azure-Migration / Cloud-Strategie: Microsoft Customer Story, Podcast \u201eTechnik aufs Ohr\u201c",
        "Patente: Europäisches Patentamt (EP3392084A1, EP3618469A1)",
    ]
    for s in sources:
        pdf.cell(5, 4, chr(8226))
        pdf.multi_cell(0, 4, s)
        pdf.ln(0.5)

    pdf.ln(5)
    pdf.set_font("DejaVu", "I", 7)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 4,
        "Hinweis: S\u00e4mtliche in diesem Dokument genannten Fakten basieren ausschlie\u00dflich auf "
        "\u00f6ffentlich zug\u00e4nglichen Quellen (Pressemitteilungen, Gesch\u00e4ftsberichte, Fachpublikationen, "
        "Podcasts, Unternehmenswebseiten, Patentregister). Es werden keine vertraulichen oder NDA-gesch\u00fctzten "
        "Informationen weitergegeben. Die Zusammenarbeit ist durch den gemeinsam gewonnenen Cloud Native "
        "Rockstars Award 2022 \u00f6ffentlich dokumentiert. Schmitz Cargobull\u00ae und TrailerConnect\u00ae "
        "sind eingetragene Marken der Schmitz Cargobull AG."
    )

    out_path = BASE / "scb_telematics_referenz.pdf"
    pdf.output(str(out_path))
    return str(out_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Generating charts...")
    c1 = create_market_share_chart()
    print(f"  -> {c1}")
    c2 = create_telematics_growth_chart()
    print(f"  -> {c2}")
    c3 = create_architecture_diagram()
    print(f"  -> {c3}")

    print("Generating PDF...")
    out = build_pdf(c1, c2, c3)
    print(f"  -> {out}")
    print("Done!")


if __name__ == "__main__":
    main()
