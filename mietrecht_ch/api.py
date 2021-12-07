from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def healthcheck():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    answer = {
        "code": 200,
        "message": "Alive",
        "timeStamp": dt_string
        }
    return answer
