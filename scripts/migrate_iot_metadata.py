#!/usr/bin/env python3
"""Einmalige Migration: pipeline/tier/contacts/outreach aus Markdown-Recherche
in leads.json überführen. Danach ist leads.json die Single Source of Truth.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

LEADS_FILE = Path(__file__).parent.parent / "leads.json"

PIPELINE_BY_TOPIC = {
    "IoT-Plattform-Entwicklung": "IoT",
    "IoT / Asset Management": "IoT",
    "IT-Outsourcing TISAX": "TISAX",
    "TISAX IT-Outsourcing Cloud/IoT/AI": "TISAX",
    "Cloud/IoT/AI IT-Outsourcing": "TISAX",
    "TISAX IT-Dienstleister Cloud/IoT/AI/Data Platform": "TISAX",
    "Risikomanagement / ETRM": "Energiehandel",
    "Betriebs- und Anlagenverwaltung": "Fernwaerme",
    "Telematik / Embedded-Software-Entwicklung": "Telematik",
}

# IoT-Pipeline: Tier-Zuordnung (Stand 15.04.2026, iot_sales_priorisierung.md)
TIERS = {
    "TIER1": [
        "Rosenberger Hochfrequenztechnik", "Mekra Lang GmbH", "ACO Severin Ahlmann",
        "GP JOULE GmbH", "Stern-Wywiol Gruppe", "Sikora AG", "Nordex SE",
        "SH Netz AG (HanseWerk)", "Harburg-Freudenberger Maschinenbau (HF Group)",
        "Fritz Winter Eisengießerei", "Klosterfrau Healthcare Group",
    ],
    "TIER2": [
        "GoodMills Deutschland GmbH", "Gentherm Präzision SE", "TROX SE",
        "FFG Flensburger Fahrzeugbau", "H. & J. Brüggen KG", "Helbako GmbH",
        "Brunsbüttel Ports GmbH", "Helm AG", "SHW Automotive GmbH",
        "SAACKE GmbH", "Tamsen Maritim GmbH", "Sweet Tec GmbH",
        "Alfred PRACHT Lichttechnik", "Limtronik", "Heinrich Rönner Gruppe",
        "Blohm+Voss",
    ],
    "TIER3": [
        "CODAN Medizintechnik", "Friesenkrone Feinkost", "Denker & Wulf AG",
    ],
    "SONDER": ["MRS Electronic GmbH"],
}

# Ansprechpartner IoT-Pipeline (Recherche 15.04.2026)
CONTACTS = {
    "Rosenberger Hochfrequenztechnik": [
        {"name": "Walter Hölblinger, MBA", "role": "CIO / Global Head of IT (seit Jan 2025)",
         "linkedin": "https://www.linkedin.com/in/walter-hoelblinger-mba/", "confidence": "HIGH"}],
    "Mekra Lang GmbH": [
        {"name": "Michael Ammon", "role": "Global Head of IT",
         "linkedin": "https://de.linkedin.com/in/michael-ammon-518890167", "confidence": "HIGH"},
        {"name": "Jorge Calderon", "role": "IT Manager", "linkedin": None, "confidence": "MEDIUM"}],
    "ACO Severin Ahlmann": [
        {"name": "Dominik Neff", "role": "CIO ACO Group (seit 09/2022, Ex-HELM AG)",
         "linkedin": "https://de.linkedin.com/in/dominik-neff-888164183", "confidence": "HIGH"},
        {"name": "Stephan Bauer", "role": "Leiter IT Service Management",
         "linkedin": "https://www.linkedin.com/in/stephan-bauer-81b2b6102/", "confidence": "MEDIUM"}],
    "GP JOULE GmbH": [
        {"name": "Kerrit Friedrichsen", "role": "CIO",
         "linkedin": "https://www.linkedin.com/in/kerrit-friedrichsen-94b047b8/", "confidence": "HIGH"}],
    "Stern-Wywiol Gruppe": [
        {"name": "Kay Postwig", "role": "Head of IT/OT",
         "linkedin": "https://de.linkedin.com/in/kay-postwig-858157281", "confidence": "HIGH"}],
    "Sikora AG": [
        {"name": "Christoph Hüniken", "role": "IT-Leiter Sikora Holding",
         "linkedin": "https://de.linkedin.com/in/christoph-h%C3%BCniken-4785721a6", "confidence": "HIGH"}],
    "Nordex SE": [
        {"name": "Stefan Ewald", "role": "CIO, Head of IT & Organization",
         "linkedin": "https://www.linkedin.com/in/stefanewald/", "confidence": "HIGH"},
        {"name": "Volker Scheeff", "role": "Director Corporate IT ERP", "linkedin": None, "confidence": "MEDIUM"}],
    "SH Netz AG (HanseWerk)": [
        {"name": "Thorsten Frye", "role": "CIO & CDO HanseWerk",
         "linkedin": "https://www.linkedin.com/in/thorsten-frye-517a44155", "confidence": "HIGH"},
        {"name": "Lisa Hebenstreit", "role": "GF Netztechnik SH Netz (Ex-Head of Digital & IT)",
         "linkedin": None, "confidence": "HIGH"}],
    "Harburg-Freudenberger Maschinenbau (HF Group)": [
        {"name": "Alexander Bodi", "role": "Head of IT (71 MA IT-Abteilung)",
         "linkedin": "https://www.linkedin.com/in/alexander-bodi-4b5ab199/", "confidence": "HIGH"}],
    "Fritz Winter Eisengießerei": [
        {"name": "Alexander Schwab", "role": "Leiter IT und Digitalisierung",
         "linkedin": "https://de.linkedin.com/in/alexander-schwab-55a931bb", "confidence": "HIGH",
         "notes": "CIO.de-Feature Feb 2026, FSAS Summit Speaker"}],
    "Klosterfrau Healthcare Group": [
        {"name": "Frank Roth", "role": "CIO / Leiter Shared Service Center IT (seit 2002)",
         "linkedin": "https://www.linkedin.com/in/frank-roth-b186b241/", "confidence": "HIGH"},
        {"name": "Lars Wilcken", "role": "Head of IT Service & Operations", "linkedin": None, "confidence": "MEDIUM"}],
    "GoodMills Deutschland GmbH": [
        {"name": "Daniel Wellenreuther", "role": "IT Business Development Manager",
         "linkedin": "https://www.linkedin.com/in/daniel-wellenreuther-23619315b/", "confidence": "MEDIUM",
         "notes": "CIO-Nachfolge nach Susanne Steffen unklar"}],
    "Gentherm Präzision SE": [
        {"name": "Ramzi Braham", "role": "VP & CIO (global, USA)", "linkedin": None, "confidence": "MEDIUM",
         "notes": "EU-IT-Manager-Stelle vakant; HR: Valentina Müller +49 8134 933-570"}],
    "TROX SE": [
        {"name": "Thomas Mosbacher", "role": "Vorstand (IT-Ressort)", "linkedin": None, "confidence": "MEDIUM"},
        {"name": "Matthias Schenk", "role": "Head of IT TROX X-Fans", "linkedin": None, "confidence": "MEDIUM"}],
    "FFG Flensburger Fahrzeugbau": [
        {"name": "Stefan Kösterke", "role": "CISO",
         "linkedin": "https://www.linkedin.com/in/stefan-k%C3%B6sterke-03a738198/", "confidence": "MEDIUM"}],
    "H. & J. Brüggen KG": [
        {"name": "Joachim Klamroth", "role": "CIO (seit 07/2021, Status 2026 prüfen)",
         "linkedin": "https://www.linkedin.com/in/klamroth/", "confidence": "MEDIUM"}],
    "Helbako GmbH": [
        {"name": "Martin Niermann", "role": "Leiter Logistik/IT",
         "linkedin": "https://www.linkedin.com/in/martin-niermann-abba3211a/", "confidence": "MEDIUM"}],
    "Brunsbüttel Ports GmbH": [
        {"name": "Frank Schnabel", "role": "GF (leitet Digitalprojekte: UniPort 4.0)",
         "linkedin": None, "confidence": "MEDIUM", "notes": "f.schnabel@schrammgroup.de"}],
    "Helm AG": [
        {"name": "Thomas Roos", "role": "CIO (Verifizierung empfohlen)",
         "linkedin": "https://de.linkedin.com/in/thomas-roos-b461573", "confidence": "MEDIUM"}],
    "SHW Automotive GmbH": [
        {"name": "Klaus Saiger", "role": "SAP Prozessmanager (Einstiegskontakt)",
         "linkedin": "https://www.linkedin.com/in/klaus-saiger-1b5394154/", "confidence": "MEDIUM"}],
    "SAACKE GmbH": [
        {"name": "(vakant)", "role": "IT-Leitung unbesetzt (Kammer zu Rheinmetall)",
         "linkedin": None, "confidence": "MEDIUM", "notes": "Telefonrecherche +49 421 6495-0"}],
    "Tamsen Maritim GmbH": [
        {"name": "Gregor Uloth", "role": "Technischer Betriebsleiter (EFRE-Projekt)",
         "linkedin": "https://www.linkedin.com/in/gregor-uloth-1159aaa7/", "confidence": "MEDIUM"}],
    "Sweet Tec GmbH": [
        {"name": "Ralf Schulzke", "role": "Kaufm. GF (SAP-Entscheider)", "linkedin": None, "confidence": "MEDIUM"}],
    "Alfred PRACHT Lichttechnik": [
        {"name": "Gerhard Hillebrand", "role": "IoT-Engineer",
         "linkedin": "https://www.linkedin.com/in/gerhard-hillebrand-3b6637134/", "confidence": "MEDIUM"}],
    "Limtronik": [
        {"name": "Gerd Ohl", "role": "GF / Industrie-4.0-Treiber (SEF-Mitgründer)",
         "linkedin": "https://www.linkedin.com/in/gerd-ohl-6a4b9b4a/", "confidence": "MEDIUM"}],
    "Heinrich Rönner Gruppe": [
        {"name": "(unbekannt)", "role": "IT in Rönner Verwaltungs-GmbH zentralisiert",
         "linkedin": None, "confidence": "LOW", "notes": "Aufhänger: FSG-Integration, ams.erp"}],
    "Blohm+Voss": [
        {"name": "Sebastian Herke", "role": "Senior IT/Data (NVL Group, jetzt Rheinmetall)",
         "linkedin": "https://www.linkedin.com/in/sebastian-herke-56295616/", "confidence": "MEDIUM"}],
    "MRS Electronic GmbH": [
        {"name": "Günther Dörgeloh", "role": "CEO & Co-Founder (Würth-Übernahme läuft)",
         "linkedin": "https://www.linkedin.com/in/g%C3%BCnther-d%C3%B6rgeloh-39a78685/", "confidence": "LOW"}],
}

# Outreach (Betreff + Aufhänger) für TIER1, aus iot_outreach_templates.md
OUTREACH = {
    "Rosenberger Hochfrequenztechnik": {
        "subject": "Vom CISO zum CIO bei Rosenberger — wie weit ist der IoT-Kern?",
        "hook": "CISO→CIO in 18 Monaten, will 'IT als Business Enabler' etablieren, CISSP + MBA."},
    "Mekra Lang GmbH": {
        "subject": "Kamerasysteme, Digital-Business-Thesis und IoT — passt das zusammen, Herr Ammon?",
        "hook": "Studiert Master Digital Business Mgmt neben dem Job; MEKRA View = eigenes IoT-Produkt."},
    "ACO Severin Ahlmann": {
        "subject": "Von HELM zu ACO: Smart Drainage als nächster IoT-Move?",
        "hook": "Neff war 2012-2019 bei HELM AG (auch in Pipeline) — warmer Intro; Entwässerung = verteilte datenlose Assets."},
    "GP JOULE GmbH": {
        "subject": "Wind + PV + Wasserstoff unter einem Asset-Dach — wie, Herr Friedrichsen?",
        "hook": "Neuer CIO; heterogenstes Anlagenportfolio (Wind, PV, H2, Laden) braucht einheitliche Asset-Sicht."},
    "Stern-Wywiol Gruppe": {
        "subject": "IT/OT in einer Rolle + 12 Firmen: Wo ist der gemeinsame Asset-Kern?",
        "hook": "Seltene IT/OT-Doppelrolle; SternConnect-Digitalisierungs-Unit; 12 Spezialfirmen, 19 Töchter."},
    "Sikora AG": {
        "subject": "Sikoras Sensorik trifft Asset-IoT — Austausch auf Augenhöhe?",
        "hook": "Sikora ist selbst Sensorhersteller (Röntgen/Laser/Kamera) — Ansprache als Peer, nicht als Verkäufer."},
    "Nordex SE": {
        "subject": "6.800 Turbinen + Acciona-SAP: die Nische neben Mindtree?",
        "hook": "Nordex OS SCADA auf Cumulocity, Mindtree-5J-Deal — Positionierung als Nischen-Ergänzung, nicht Ersatz."},
    "SH Netz AG (HanseWerk)": {
        "subject": "24 Jahre HanseWerk Natur — Gespräch zur LoRaWAN-Asset-Brücke?",
        "hook": "Direkte Referenz: 24 Jahre Betriebs-/Anlagenverwaltung für HanseWerk Natur; LoRaWAN 60→400 Antennen."},
    "Harburg-Freudenberger Maschinenbau (HF Group)": {
        "subject": "ECM steht — wie nah ist HF Mixing an einer Asset-Schicht?",
        "hook": "ACTIWARE/ELO-ECM läuft; 4 Business Units mit unterschiedlichen Maschinenparks = Asset-Lücke."},
    "Fritz Winter Eisengießerei": {
        "subject": "Nach 75% IT-Leerlauf: Was macht der Asset-Kern jetzt, Herr Schwab?",
        "hook": "CIO.de-Feature Feb 2026; uSCALE/NetApp gelöst, SAP konsolidiert — nächste Ebene ist Maschinensensorik/OEE."},
    "Klosterfrau Healthcare Group": {
        "subject": "2002–heute: Ähnliche Langstrecke — Asset-IoT für Berlin/Lüchow?",
        "hook": "Roth ist CIO seit 2002 (24 Jahre — wie unsere HanseWerk-Referenz); S/4HANA live, Picavi Smart Glasses."},
}

REMOVE = ["Nordex SE Rostock"]


def main() -> None:
    data = json.loads(LEADS_FILE.read_text())
    leads = data["leads"]

    # 1. Duplikat entfernen
    before = len(leads)
    leads = [l for l in leads if l["company"]["name"] not in REMOVE]
    data["leads"] = leads
    print(f"Entfernt: {before - len(leads)} Duplikat(e)")

    # 2. Pipeline aus Topic ableiten (wo noch nicht gesetzt)
    n_pipeline = 0
    for lead in leads:
        if lead.get("pipeline"):
            continue
        tr = lead.get("topic_relevance") or {}
        topic = (tr.get("topic_affinity") or {}).get("topic", "")
        pipeline = PIPELINE_BY_TOPIC.get(topic)
        if pipeline:
            lead["pipeline"] = pipeline
            n_pipeline += 1
    print(f"Pipeline gesetzt: {n_pipeline}")

    # 3. Tier, Kontakte, Outreach
    n_tier = n_contact = n_outreach = 0
    for lead in leads:
        name = lead["company"]["name"]
        for tier, names in TIERS.items():
            if any(n == name or n in name or name in n for n in names):
                lead["tier"] = tier
                n_tier += 1
                break
        for key, contacts in CONTACTS.items():
            if key == name or key in name or name in key:
                lead["contact_persons"] = contacts
                n_contact += 1
                break
        for key, outreach in OUTREACH.items():
            if key == name or key in name or name in key:
                lead["outreach"] = outreach
                n_outreach += 1
                break

    print(f"Tier gesetzt: {n_tier} | Kontakte: {n_contact} | Outreach: {n_outreach}")

    LEADS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("leads.json aktualisiert.")


if __name__ == "__main__":
    main()
