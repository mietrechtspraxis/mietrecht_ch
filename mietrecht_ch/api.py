from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

@frappe.whitelist(allow_guest=True)
def healthcheck():
    answer = {
        "code": 200,
        "message": "Alive"
        }
    return answer



