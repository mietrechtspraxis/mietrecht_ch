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
                }
            ]
        }
    ]