from __future__ import unicode_literals
from frappe import _


def get_data():
    return[
        {
            "label": _("Heiz-und Nebenkosten"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Meteostationen",
                    "label": _("Meteostationen"),
                    "description": _("Meteostationen")
                },
                {
                    "type": "doctype",
                    "name": "Meteodaten",
                    "label": _("Meteodaten"),
                    "description": _("Meteodaten")
                },
                {
                    "type": "doctype",
                    "name": "Heizolpreise",
                    "label": _("Heizölpreise Liste"),
                    "description": _("Heizölpreise Liste")
                },
                {
                    "type": "doctype",
                    "name": "Heizgradtagzahlen",
                    "label": _("Heizgradtagzahlen Liste"),
                    "description": _("Heizgradtagzahlen Liste")
                },
                {
                    "type": "doctype",
                    "name": "Akkumulierte Temperaturdifferenzen",
                    "label": _("Akkumulierte Temperaturdifferenzen Liste"),
                    "description": _("Akkumulierte Temperaturdifferenzen Liste")
                },
                {
                    "type": "doctype",
                    "name": "Kuhlgradtagzahlen",
                    "label": _("Kühlgradtagzahlen Liste"),
                    "description": _("Kühlgradtagzahlen Liste")
                }
            ]
        },
        {
            "label": _("Lebensdauertabelle"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "LebensdauerGruppe",
                    "label": _("Stichworte"),
                    "description": _("Stichworte")
                },
                #{
                #    "type": "doctype",
                #    "label": _("Neue Gruppe"),
                #    "name": "LebensdauerGruppe",
                #    "description": _("Neue Gruppe"),
                #    "link": _("Form/LebensdauerGruppe/New LebensdauerGruppe 1")
                #},
                {
                    "type": "doctype",
                    "name": "LebensdauerObjekte",
                    "label": _("Objekte"),
                    "description": _("Objekte")
                },
                #{
                #    "type": "doctype",
                #    "name": "LebensdauerObjekte",
                #    "label": _("Neue Objekte"),
                #    "description": _("Neue Objekte"),
                #    "link": _("Form/LebensdauerObjekte/New LebensdauerObjekte 1")
                #},
            ]
        },
        {
            "label": _("Landesindex"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Aktualisierungsdaten",
                    "label": _("Aktualisierungsdaten Liste"),
                    "description": _("Aktualisierungsdaten Liste")
                },
                {
                    "type": "doctype",
                    "name": "Aktualisierungsdaten",
                    "label": _("Neue Aktualisierungsdaten"),
                    "description": _("Neue Aktualisierungsdaten"),
                    "link": _("Form/Aktualisierungsdaten/New Aktualisierungsdaten 1")
                },
                {
                    "type": "doctype",
                    "name": "Teuerung",
                    "label": _("Teuerung Liste"),
                    "description": _("Teuerung Liste")
                },
                {
                    "type": "doctype",
                    "name": "Teuerung",
                    "label": _("Neue Teuerung"),
                    "description": _("Neue Teuerung"),
                    "link": _("Form/Teuerung/New Teuerung 1")
                },
                {
                    "type": "doctype",
                    "name": "TeuerungBasis",
                    "label": _("Teuerung Basis Liste"),
                    "description": _("Teuerung Basis Liste")
                },
                {
                    "type": "doctype",
                    "name": "TeuerungBasis",
                    "label": _("Neue TeuerungBasis"),
                    "description": _("Neue Teuerung Basis"),
                    "link": _("Form/TeuerungBasis/New TeuerungBasis 1")
                }
            ]
        },
        {
            "label": _("Hypo-Referenzzins"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "HypoReferenzzins",
                    "label": _("Hypo-Referenzzins Liste"),
                    "description": _("Hypo-Referenzzins Liste")
                },
                {
                    "type": "doctype",
                    "name": "HypoReferenzzins",
                    "label": _("Neue Hypo-Referenzzins"),
                    "description": _("Neue Hypo-Referenzzins"),
                    "link": _("Form/HypoReferenzzins/New HypoReferenzzins 1")
                },
                {
                    "type": "doctype",
                    "name": "Hypothekarzins",
                    "label": _("Hypothekarzins Liste"),
                    "description": _("Hypothekarzins Liste")
                },
                {
                    "type": "doctype",
                    "name": "Hypothekarzins",
                    "label": _("Neue Hypothekarzins"),
                    "description": _("Neue Hypothekarzins"),
                    "link": _("Form/Hypothekarzins/New Hypothekarzins 1")
                },
                {
                    "type": "doctype",
                    "name": "Hypothekarzins Aktualisierungsdaten",
                    "label": _("Nächste Hypothekarzins Aktualisierungsdaten"),
                    "description": _("Nächste Hypothekarzins Aktualisierungsdaten"),
                    "link": _("Form/Hypothekarzins Aktualisierungsdaten")
                }
            ]
        },
        {
            "label": _("Einstellungen"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Wetterstationen",
                    "label": _("Wetterstationen"),
                    "description": _("Wetterstationen")
                },

                #{
                #    "type": "doctype",
                #    "name": "Wetterstationen",
                #    "label": _("Neue Wetterstationen"),
                #    "description": _("Neue Wetterstationen"),
                #    "link": _("Form/Wetterstationen/New Wetterstationen 1")
                #}
            ]
        },
        {
            "label": _("Stichworte"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Stichworte",
                    "label": _("Stichworte Liste"),
                    "description": _("Stichworte Liste")
                },
                {
                    "type": "doctype",
                    "name": "Stichworte",
                    "label": _("Neue Stichworte"),
                    "description": _("Neue Stichworte"),
                    "link": _("Form/Stichworte/New Stichworte 1")
                }
            ]
        },
        {
            "label": _("E-Book"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Voucher",
                    "label": _("Voucher Liste"),
                    "description": _("Voucher Liste")
                },
                {
                    "type": "doctype",
                    "name": "Pak",
                    "label": _("PAK Liste"),
                    "description": _("PAK Liste")
                }
            ]
        },
        {
            "label": _("Entscheide"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Entscheid",
                    "label": _("Entscheide Liste"),
                    "description": _("Entscheide Liste")
                },
                {
                    "type": "doctype",
                    "name": "SearchLog",
                    "label": _("Entscheidsuche (Protokoll)"),
                    "description": _("Entscheidsuche"),
                }
            ]
        },
        {
            "label": _("Gesetze"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Gesetze",
                    "label": _("Gesetze Liste"),
                    "description": _("Gesetze Liste")
                },
                {
                    "type": "doctype",
                    "name": "Gesetze",
                    "label": _("Gesetz hinzufügen"),
                    "description": _("Gesetz hinzufügen"),
                    "link": _("Form/Gesetze/New Gesetze 0")
                }
            ]
        },
        {
            "label": _("CMS"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "CMS Content",
                    "label": _("CMS Content ✍️"),
                    "description": _("CMS Content")
                },
                {
                    "type": "doctype",
                    "name": "CMS Actions",
                    "label": _("CMS Link und Datei (🔗) und Button (🆒)"),
                    "description": _("CMS Aktionen")
                }
            ]
        },
        {
            "label": _("Short URL/Weiterleitung"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Short URL",
                    "label": _("Liste der Weiterleitungen"),
                    "description": _("Liste der Weiterleitungen")
                },
                {
                    "type": "doctype",
                    "name": "Short URL",
                    "label": _("Weiterleitung hinzufügen"),
                    "description": _("Weiterleitung hinzufügen"),
                    "link": _("Form/Short URL/New Kurze URL 0")
                }
            ]
        },
        {
            "label": _("Kurse und Weiterbildungen"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Kurse und Seminare",
                    "label": _("Kurse und Weiterbildungen"),
                    "description": _("Kurse und Weiterbildungen")
                }
            ]
        },
        {
            "label": _("CMS Actions"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "CMS Actions",
                    "label": _("CMS Aktionen"),
                    "description": _("CMS Aktionen")
                },
                {
                    "type": "doctype",
                    "name": "CMS Actions",
                    "label": _("Neue CMS Aktionen"),
                    "description": _("New CMS Aktionen"),
                    "link": _("Form/CMS Actions/New CMS Aktionen 0")
                }
            ]
        },
        {
            "label": _("Bestellungen: Shop und Abo"),
            "icon": "fa fa-check-square",
            "items": [
                {
                    "type": "doctype",
                    "name": "Antwort auf das Formular",
                    "label": _("Antwort auf das Formular"),
                    "description": _("Antwort auf das Formular"),
                }
            ]
        }
    ]
