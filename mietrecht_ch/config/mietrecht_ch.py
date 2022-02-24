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
                    "name": "Heizolpreise",
                    "label": _("Heizolpreise Liste"),
                    "description": _("Heizolpreise Liste")
                },
                {
                    "type": "doctype",
                    "name": "Heizolpreise",
                    "label": _("Neue Heizolpreise"),
                    "description": _("Neue Heizolpreise"),
                    "link": _("Form/Heizolpreise/New Heizolpreise 1")
                },
                {
                    "type": "doctype",
                    "name": "Heizgradtagzahlen",
                    "label": _("Heizgradtagzahlen Liste"),
                    "description": _("Heizgradtagzahlen Liste")
                },
                {
                    "type": "doctype",
                    "name": "Heizgradtagzahlen",
                    "label": _("Neue Heizgradtagzahlen"),
                    "description": _("Neue Heizgradtagzahlen"),
                    "link": _("Form/Heizgradtagzahlen/New Heizgradtagzahlen 1")
                }
            ]
        },
        {
            "label": _("Einstellungen"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Ortschaft",
                    "label": _("Ortschaft Liste"),
                    "description": _("Ortschaft Liste")
                },
                {
                    "type": "doctype",
                    "name": "Ortschaft",
                    "label": _("Neue Ortschaft"),
                    "description": _("Neue Ortschaft"),
                    "link": _("Form/Ortschaft/New Ortschaft 1")
                }
            ]
        }
    ]