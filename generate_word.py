#!/usr/bin/env python3
"""Generate Word document with outreach templates for TIER 1 leads."""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

LEADS = [
    {
        'firma': 'Rosenberger Hochfrequenztechnik',
        'person': 'Walter Hoelblinger, MBA',
        'rolle': 'CIO / Global Head of IT (seit Jan 2025)',
        'score': '75.2%',
        'betreff': 'Vom CISO zum CIO bei Rosenberger – wie weit ist der IoT-Kern?',
        'nachricht': (
            'Lieber Herr Hoelblinger,\n\n'
            'vom CISO zum CIO in 18 Monaten – und parallel eine HF-Elektronikfertigung '
            'mit globalem Footprint zu digitalisieren. Respekt.\n\n'
            'Sie haben betont, IT muesse "Business Enabler" werden. Bei einem Unternehmen, '
            'das physische Produkte an 14.000 MA-Standorten weltweit fertigt, ist der '
            'Asset-Kern der kuerzeste Weg dorthin.\n\n'
            'Wir haben genau diese Schnittstelle – Betrieb/Produktion trifft IT-Plattform '
            '– ueber 24 Jahre fuer einen Energieversorger gebaut. Die Kurzfassung in '
            '2 Minuten: [VIDEO-LINK]\n\n'
            'Falls Sie in Ihrer IT-Roadmap einen Asset-Layer brauchen, der Ihre '
            'CISSP-Qualitaet nicht aufweicht: gerne ein kurzes Gespraech.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'CISO→CIO Wechsel in 18 Monaten, "IT als Business Enabler", CISSP + MBA IT Mgmt',
    },
    {
        'firma': 'Mekra Lang GmbH',
        'person': 'Michael Ammon',
        'rolle': 'Global Head of IT',
        'score': '77.1%',
        'betreff': 'Kamerasysteme, Digital-Business-Thesis und IoT – passt das zusammen, Herr Ammon?',
        'nachricht': (
            'Lieber Herr Ammon,\n\n'
            'als Global Head of IT einen Master in Digital Business Management neben dem '
            'Job zu machen – das ist die Art Neugierde, die selten wird, sobald man den '
            'Titel hat.\n\n'
            'Was mir auffiel: Mit MEKRA View und den digitalen Rueckspiegeln sind Sie '
            'bereits IoT-Hersteller. Haben Sie intern eine Asset-Plattform, die sowohl '
            'die Produktionsanlagen in Ergersheim als auch die Feldtelemetrie der '
            'Kamerasysteme zusammenbringt?\n\n'
            'Wir haben 24 Jahre an genau dieser Schnittstelle gebaut – fuer einen '
            'Energieversorger mit 1.000+ dezentralen Anlagen. 2-Minuten-Video: [VIDEO-LINK]\n\n'
            'Falls es Thesis-tauglich ist, umso besser.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'Studiert Master Digital Business neben dem Job. MEKRA View = IoT-Produkt.',
    },
    {
        'firma': 'ACO Severin Ahlmann',
        'person': 'Dominik Neff',
        'rolle': 'CIO, ACO Group (seit Sep 2022, Ex-HELM AG)',
        'score': '66.5%',
        'betreff': 'Von HELM zu ACO: Smart Drainage als naechster IoT-Move?',
        'nachricht': (
            'Lieber Herr Neff,\n\n'
            'Ihre Station bei HELM AG vor ACO macht neugierig: beides Familienunternehmen, '
            'beides IT-Strategien, die mehr verlangen als SAP-Konsolidierung.\n\n'
            'Bei ACO sehe ich einen Hebel, den viele uebersehen: Entwaesserungstechnik '
            'ist datenlos im Betrieb – aber die Anlagen (Pumpstationen, Rueckhaltebecken, '
            'Abscheider) sind hochkritisch und ueber Staedte verteilt. Eine leichte '
            'Asset-Plattform darueber veraendert die Servicequalitaet fundamental.\n\n'
            'Wir haben so etwas 24 Jahre fuer einen Energieversorger mit tausenden '
            'dezentralen Anlagen aufgebaut. 2 Minuten: [VIDEO-LINK]\n\n'
            'Ist "Smart Drainage" bei Ihnen schon auf der Roadmap – oder noch ein '
            'weisses Feld?\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'Ex-HELM AG (2012–2019). Entwaesserungstechnik = verteilte, datenlose Infrastruktur.',
    },
    {
        'firma': 'GP JOULE GmbH',
        'person': 'Kerrit Friedrichsen',
        'rolle': 'CIO, GP JOULE Gruppe',
        'score': '64.2%',
        'betreff': 'Wind + PV + Wasserstoff unter einem Asset-Dach – wie, Herr Friedrichsen?',
        'nachricht': (
            'Lieber Herr Friedrichsen,\n\n'
            'GP JOULE ist einer der wenigen Player, die wirklich ueber alle erneuerbaren '
            'Klassen arbeiten – Wind, PV, H2-Elektrolyse, Ladeinfrastruktur. Strategisch '
            'beeindruckend und operativ... sportlich. Jede Anlagenklasse bringt eigene '
            'Leitsysteme, Protokolle, Wartungszyklen.\n\n'
            'Als CIO werden Sie frueher oder spaeter an die Frage kommen: Einheitliche '
            'Asset-Sicht ueber alle Gewerke – oder Silos akzeptieren?\n\n'
            'Wir haben 24 Jahre an genau dieser Bruecke gebaut – fuer einen '
            'Energieversorger mit Waerme-, Strom- und Dampfanlagen unter einem Dach. '
            'In 2 Minuten: [VIDEO-LINK]\n\n'
            'Fuer eine Runde Sparring gerne verfuegbar.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'Neuer CIO. Wind+PV+H2+E-Mobility = heterogenstes Asset-Portfolio.',
    },
    {
        'firma': 'Stern-Wywiol Gruppe',
        'person': 'Kay Postwig',
        'rolle': 'Head of IT/OT',
        'score': '62.6%',
        'betreff': 'IT/OT in einer Rolle + 12 Firmen: Wo ist der gemeinsame Asset-Kern?',
        'nachricht': (
            'Lieber Herr Postwig,\n\n'
            '"Head of IT/OT" als Einzeltitel – das ist eine Raritaet. In den meisten '
            'Konzernen sitzen die Themen in getrennten Silos. Dass Stern-Wywiol das '
            'zusammenlegt und mit SternConnect eine eigene Digi-Einheit dranhaengt, zeigt '
            'wohin die Reise geht.\n\n'
            'Was mich interessiert: Wie ziehen Sie den Asset-Kern ueber 12 Spezialfirmen '
            'konsistent durch? Jede Einheit hat eigene Produktionsrealitaet – '
            'Emulgatoren, Enzyme, Dragees – und jeder OT-Stack ist anders.\n\n'
            'Wir haben 24 Jahre eine Plattform gebaut, die ueber heterogene Anlagen ein '
            'einheitliches Asset- und Betriebsbild liefert. 2 Minuten: [VIDEO-LINK]\n\n'
            'Falls das anschlussfaehig zu SternConnect ist – ein kurzes Gespraech?\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'Seltene IT/OT-Doppelrolle. SternConnect Digi-Unit. 12 Spezialfirmen.',
    },
    {
        'firma': 'Sikora AG',
        'person': 'Christoph Hueniken',
        'rolle': 'IT-Leiter, Sikora Holding',
        'score': '60.5%',
        'betreff': 'Sikoras Sensorik trifft Asset-IoT – Austausch auf Augenhoehe?',
        'nachricht': (
            'Lieber Herr Hueniken,\n\n'
            'Sikora baut seit Jahrzehnten Sensorik, die in Kundenanlagen weltweit '
            'Qualitaet sichert – Roentgen, Laser, Kameras. Sie verstehen Messwerte und '
            'IoT-Datenstrroeme aus erster Hand.\n\n'
            'Deshalb spreche ich Sie weniger als Verkaeufer an, sondern auf Augenhoehe: '
            'Wir haben ueber 24 Jahre eine Asset-Plattform fuer einen Energieversorger '
            'entwickelt – mit sehr aehnlichen Mustern (verteilte Sensoren, schmale '
            'Bandbreite, Nachweispflichten).\n\n'
            '2 Minuten Einblick: [VIDEO-LINK]\n\n'
            'Falls Sie intern die Bruecke von Produkt-Sensorik zu Anlagen-Management '
            'denken – oder einfach Interesse an einem Sparring: gerne.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'Sikora ist selbst Sensorhersteller. Sparring auf Augenhoehe.',
    },
    {
        'firma': 'Nordex SE',
        'person': 'Stefan Ewald',
        'rolle': 'CIO, Head of IT & Organization',
        'score': '57.9%',
        'betreff': '6.800 Turbinen + Acciona-SAP: die Nische neben Mindtree?',
        'nachricht': (
            'Lieber Herr Ewald,\n\n'
            '6.800+ Turbinen auf Cumulocity, 5-Jahres-Programm mit Mindtree, parallel '
            'die Acciona-Integration in SAP – Ihre Agenda ist eine der vollsten im '
            'deutschen CIO-Kreis.\n\n'
            'Ich schreibe nicht als Ersatz fuer Mindtree, sondern als moegliche '
            'Ergaenzung daneben: Wir haben 24 Jahre an einer Asset- und '
            'Betriebsfuehrungsplattform gebaut. Unsere Staerke sitzt dort, wo Nordex OS '
            'SCADA endet und das Betriebs-/Wartungs-ERP anfaengt – die Bruecke dazwischen.\n\n'
            '2 Minuten, damit Sie selbst beurteilen ob das einen zweiten Blick wert ist: '
            '[VIDEO-LINK]\n\n'
            'Falls Acciona-Integration gerade Asset-Daten auf Ihren Tisch drueckt – '
            'gerne ein kurzer Call.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'Cumulocity SCADA, 6.800+ Turbinen, Mindtree-5J-Deal, Acciona-Integration.',
    },
    {
        'firma': 'SH Netz AG / HanseWerk',
        'person': 'Thorsten Frye',
        'rolle': 'CIO & CDO, HanseWerk',
        'score': '56.9%',
        'betreff': '24 Jahre HanseWerk Natur – Gespraech zur LoRaWAN-Asset-Bruecke?',
        'nachricht': (
            'Lieber Herr Frye,\n\n'
            'ich melde mich aus einem ungewoehnlichen Grund: Wir haben 24 Jahre die '
            'Betriebs- und Anlagenverwaltung fuer HanseWerk Natur gebaut – Architektur, '
            'Entwicklung, Testing, Betrieb. Kein Produkt aus der Tuete, sondern gemeinsam '
            'gewachsen.\n\n'
            'Dass SH Netz jetzt mit LoRaWAN ueber 60 Antennen auf Strommasten Richtung '
            '400 skaliert und DXC das Smart Metering aufsetzt, zeigt: der Sensoren-Layer '
            'steht. Die spannende Frage ist die darueber – wie bringen Sie die '
            'Feldtelemetrie in die Asset- und Betriebsfuehrung, ohne parallel zur '
            'HanseWerk Natur eine zweite Plattform zu bauen?\n\n'
            '2 Minuten, wie wir Strom-Seite und Waerme-Seite gemeinsam denken wuerden: '
            '[VIDEO-LINK]\n\n'
            'Falls ein Austausch – auch intern mit Frau Hebenstreit – Sinn macht: '
            'jederzeit.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': '24 Jahre HanseWerk Natur! LoRaWAN 60->400 Antennen. Bridge Strom/Waerme.',
    },
    {
        'firma': 'HF Group (Harburg-Freudenberger)',
        'person': 'Alexander Bodi',
        'rolle': 'Head of IT (71 MA)',
        'score': '55.5%',
        'betreff': 'ECM steht – wie nah ist HF Mixing an einer Asset-Schicht?',
        'nachricht': (
            'Lieber Herr Bodi,\n\n'
            '71 MA IT, ACTIWARE/ELO-ECM im Aufbau, vier Business Units (Mixing, TireTech, '
            'Press+LipidTech, FoodTech) mit jeweils komplett unterschiedlichen '
            'Maschinenparks – und die Possehl Digital Conference im Ruecken.\n\n'
            'Ein Muster, das wir oft sehen: Sobald das ECM strukturiert ist und die '
            'Dokumentationsfluesse laufen, wird die naechste Luecke sichtbar – das '
            'einheitliche Asset-Bild ueber die Geschaeftsbereiche. Gerade bei vier sehr '
            'unterschiedlichen Maschinenbau-Segmenten ein Hebel.\n\n'
            'Wir haben 24 Jahre an einer solchen Asset-Plattform gebaut. 2-Min-Video: '
            '[VIDEO-LINK]\n\n'
            'Fuer ein 30-Min-Sparring – ob intern oder extern der naechste Schritt ist '
            '– gerne.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': '71 MA IT, ECM mit ACTIWARE/ELO, 4 Business Units mit versch. Maschinenparks.',
    },
    {
        'firma': 'Fritz Winter Eisengiesserei',
        'person': 'Alexander Schwab',
        'rolle': 'Leiter IT und Digitalisierung',
        'score': '57.5%',
        'betreff': 'Nach 75% IT-Leerlauf: Was macht der Asset-Kern jetzt, Herr Schwab?',
        'nachricht': (
            'Lieber Herr Schwab,\n\n'
            'Ihr CIO.de-Beitrag "75% IT-Leerlauf – wie Fritz Winter tote Ressourcen '
            'eliminiert" war einer der konkretesten Praxisberichte dieses Jahres. '
            'uSCALE MetroCluster, Pay-per-Use, zwei RZ – saubere Arbeit.\n\n'
            'Was mich neugierig macht: Infrastruktur-Schicht geloest, SAP konsolidiert. '
            'Die naechste Grenze liegt meistens dort, wo der Giessereiprozess selbst Daten '
            'liefert – Maschinensensorik, OEE, Predictive Maintenance jenseits von ERP.\n\n'
            'Wir haben eine Asset- und Betriebsfuehrungsplattform, die 24 Jahre mit einem '
            'Energieversorger mitgewachsen ist. 2 Minuten: [VIDEO-LINK]\n\n'
            'Falls Sie fuer die naechste Ebene – Asset-Daten, nicht nur Ressourcen – '
            'einen Sparring-Partner suchen: gerne ein Follow-up zum uSCALE-Interview.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'CIO.de-Feature Feb 2026 "75% IT-Leerlauf". NetApp uSCALE. SAP konsolidiert.',
    },
    {
        'firma': 'Klosterfrau Healthcare Group',
        'person': 'Frank Roth',
        'rolle': 'CIO / Leiter Shared Service Center IT (seit 2002)',
        'score': '52.0%',
        'betreff': '2002–heute: Aehnliche Langstrecke – Asset-IoT fuer Berlin/Luechow?',
        'nachricht': (
            'Lieber Herr Roth,\n\n'
            'seit 2002 bei Klosterfrau – und in dieser Zeit RZ-Neubau, S/4HANA-Migration '
            'und Picavi Smart Glasses in die sterilen Linien nach Berlin gebracht. Das ist '
            'die Art Langstrecken-Arbeit, die selten genug gemacht wird.\n\n'
            'Wir haben ueber 24 Jahre einen sehr aehnlichen Weg an der Seite eines '
            'Energieversorgers gebaut – Architektur, Betrieb, Weiterentwicklung aus '
            'einem Guss.\n\n'
            'Neugierige Frage: Nach S/4HANA und Picavi – ist der naechste Schritt ein '
            'einheitlicher Asset-Layer ueber die drei Standorte (Berlin, Luechow, Koeln) '
            'und die sterile Abfuellung? 2 Minuten Video: [VIDEO-LINK]\n\n'
            'Fuer ein Sparring – CIO zu Software-Partner, beide mit '
            'Langstrecken-Perspektive – jederzeit gerne.\n\n'
            'Beste Gruesse'
        ),
        'aufhaenger': 'CIO seit 2002 (24 Jahre wie wir!). S/4HANA seit 2021. Picavi Smart Glasses.',
    },
]


def main():
    doc = Document()

    # Styles
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10)

    # Title
    title = doc.add_heading('IoT Outreach-Vorlagen', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('TIER 1 – 11 personalisierte LinkedIn/Email-Anschreiben')
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(100, 100, 100)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run('Stand: 15.04.2026 | [VIDEO-LINK] = Link zum IoT-Video einsetzen')
    run2.font.size = Pt(9)
    run2.font.italic = True
    run2.font.color.rgb = RGBColor(150, 150, 150)

    doc.add_page_break()

    # One section per lead
    for i, lead in enumerate(LEADS):
        # Header
        h = doc.add_heading(f'{i + 1}. {lead["firma"]}', level=1)

        # Info table
        table = doc.add_table(rows=3, cols=2)
        table.style = 'Light Grid Accent 1'
        table.alignment = WD_TABLE_ALIGNMENT.LEFT
        cells = [
            ('Ansprechpartner', f'{lead["person"]} – {lead["rolle"]}'),
            ('Score', lead['score']),
            ('Aufhaenger', lead['aufhaenger']),
        ]
        for row_idx, (key, val) in enumerate(cells):
            table.cell(row_idx, 0).text = key
            table.cell(row_idx, 1).text = val
            # Bold key
            for p in table.cell(row_idx, 0).paragraphs:
                for run in p.runs:
                    run.bold = True

        doc.add_paragraph()

        # Betreff
        p_subj = doc.add_paragraph()
        run_label = p_subj.add_run('Betreff: ')
        run_label.bold = True
        run_label.font.size = Pt(11)
        run_subj = p_subj.add_run(lead['betreff'])
        run_subj.italic = True
        run_subj.font.size = Pt(11)
        run_subj.font.color.rgb = RGBColor(41, 65, 122)

        # Nachricht
        doc.add_paragraph()
        p_msg_label = doc.add_paragraph()
        run_ml = p_msg_label.add_run('Nachricht:')
        run_ml.bold = True

        # Message text with proper paragraphs
        for para_text in lead['nachricht'].split('\n\n'):
            if para_text.strip():
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run(para_text.strip())
                run.font.size = Pt(10)
                # Highlight VIDEO-LINK
                if '[VIDEO-LINK]' in para_text:
                    # Can't highlight inline easily, just make the paragraph slightly different
                    pass

        if i < len(LEADS) - 1:
            doc.add_page_break()

    # Final page: Quick reference table
    doc.add_page_break()
    doc.add_heading('Quick Reference – Alle Betreffs', level=1)

    table2 = doc.add_table(rows=len(LEADS) + 1, cols=4)
    table2.style = 'Light Grid Accent 1'
    headers = ['Nr', 'Firma', 'Empfaenger', 'Betreff']
    for col, h in enumerate(headers):
        table2.cell(0, col).text = h
        for p in table2.cell(0, col).paragraphs:
            for run in p.runs:
                run.bold = True

    for i, lead in enumerate(LEADS):
        table2.cell(i + 1, 0).text = str(i + 1)
        table2.cell(i + 1, 1).text = lead['firma']
        table2.cell(i + 1, 2).text = lead['person']
        table2.cell(i + 1, 3).text = lead['betreff']

    out = 'iot_outreach_vorlagen.docx'
    doc.save(out)
    print(f'Word erstellt: {out} ({len(LEADS)} Vorlagen, {len(LEADS) + 2} Seiten)')


if __name__ == '__main__':
    main()
