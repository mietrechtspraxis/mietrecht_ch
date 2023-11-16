import frappe

@frappe.whitelist(allow_guest=True)
def get_shop_products():
    
    products = [
        {
        "description": "<div>Abonnemente für unsere Periodika.</div>",
        "item_group": "Abonnement",
        "items": [
                        {
                "description": "<div>A6-Taschenbroschüre</div><div>(80 Seiten)</div><div>neuste Ausgabe, 2019</div>",
                "item_code": "BROS-PLT",
                "item_name": "Broschüre Paritätische Lebensdauertabelle",
                "image": "/files/lebensd_titel_50px.gif",
                "rate": 10
            },
            {
                "description": "<div>A6-Taschenbroschüre</div><div>(146 Seiten)</div><div>neuste Ausgabe, 2022 (Nachdruck)</div>",
                "item_code": "BROS-MGV",
                "item_name": "Broschüre Das Mietrecht: Gesetz und Verordnung",
                "image": "/files/gesetz_titel_50px.gif",
                "rate": 10
            },
        ]
        },
        {
        "description": "<div>Diese Broschüren sind Abonnements-Bestandteil von 'mietrechtspraxis/mp'.</div>",
        "item_group": "Broschüren (mp)",
        "items": [
        {
        "description": "<div>A6-Taschenbroschüre</div><div>(80 Seiten)</div><div>neuste Ausgabe, 2019</div>",
        "item_code": "BROS-PLT",
        "item_name": "Broschüre Paritätische Lebensdauertabelle",
        "image": "/files/lebensd_titel_50px.gif",
        "rate": 10
        },
        {
        "description": "<div>A6-Taschenbroschüre</div><div>(146 Seiten)</div><div>neuste Ausgabe, 2022 (Nachdruck)</div>",
        "item_code": "BROS-MGV",
        "item_name": "Broschüre Das Mietrecht: Gesetz und Verordnung",
        "image": "/files/gesetz_titel_50px.gif",
        "rate": 10
        },
        {
        "description": "<div>A6-Taschenbroschüre</div><div>(128 Seiten)</div><div>aktuelle Ausgabe, erscheint jeden April</div>",
        "item_code": "BROS-DAM",
        "item_name": "Broschüre Daten und Adressen zum Mietrecht",
        "image": None,
        "rate": 10
        }
        ]
        },
        {
        "description": "<div>Mietrechtliche Fachliteratur</div>",
        "item_group": "Fachliteratur",
        "items": [
        {
        "description": "<div>AutorInnenkollektiv</div><div>(1216 Seiten)</div><div>2022, 10. Aufl.</div>",
        "item_code": "BUCH-MFP-2022",
        "item_name": "Buch Mietrecht für die Praxis, 10. Aufl., 2022",
        "image": "/files/Cover_MfP10_50px.png",
        "rate": 247
        },
        {
        "description": "<div>Ruedi Spöndlin</div><div>(184 Seiten)</div><div>2018, 8. Aufl. </div>",
        "item_code": "BUCH-MFM-2018",
        "item_name": "Buch Mietrecht für Mieterinnen und Mieter, 8. Aufl., 2018",
        "image": None,
        "rate": 39
        },
        {
        "description": "<div>(1354 Seiten)</div><div>2018, 4. Aufl.</div>",
        "item_code": "FRVE-SVI-2018",
        "item_name": "Buch Das schweizerische Mietrecht, SVIT-Kommentar, 4. Aufl., 2018",
        "image": None,
        "rate": 338
        },
        {
        "description": "<div>Richard Püntener</div><div>(487 Seiten)</div><div>2016, 1. Aufl.</div>",
        "item_code": "FRVE-ZPO-2016",
        "item_name": "Buch Zivilprozessrecht für Mietrechtspraxis, 1. Aufl., 2016",
        "image": None,
        "rate": 98
        },
        {
        "description": "<div>P. Higi, A. Bühlmann, C. Wildisen</div><div>(810 Seiten)</div><div>2019, 5. Aufl.</div>",
        "item_code": "FRVE-HIG-2019",
        "item_name": "Buch Die Miete – Vorbemerkungen zum 8. Titel (Art. 253 - 273c OR), Peter Higi, 5. Aufl., 2022",
        "image": None,
        "rate": 348
        }
        ]
        },
        {
        "description": "<div>Unsere Formulare erleichtern Ihre Arbeit rund um das Mieten und Wohnen.</div>",
        "item_group": "Formulare (mp)",
        "items": [
        {
        "description": "<div>Formular </div><div>(mit Durchschlag)</div>",
        "item_code": "FORM-MIE",
        "item_name": "Formular Mietvertrag für Wohnräume",
        "image": None,
        "rate": 5
        },
        {
        "description": "<div>Formular </div><div>(mit Durchschlag)</div>",
        "item_code": "FORM-UNT",
        "item_name": "Formular Untermietvertrag",
        "image": None,
        "rate": 5
        },
        {
        "description": "<div>Formular </div><div>(mit Durchschlag)</div>",
        "item_code": "FORM-MAE-01",
        "item_name": "Formular Abnahmeprotokoll/Mängelliste (Set)",
        "image": None,
        "rate": 6
        },
        {
        "description": "<div>Formularblock à 10 Exemplare </div><div>(jeweils mit Durchschlag)</div>",
        "item_code": "FORM-MAE-10",
        "item_name": "Formular Abnahmeprotokoll/Mängelliste (Block)",
        "image": None,
        "rate": 60
        }
        ]
        }
        ]

    
    return products