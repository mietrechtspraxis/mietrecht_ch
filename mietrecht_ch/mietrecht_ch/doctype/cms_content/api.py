import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json

@frappe.whitelist(allow_guest=True)
def get_by_key(key = None):
    if (key == None):
        raise BadRequestException("Please provide the parameter key")

    try:
        content = frappe.get_doc(
            'CMS Content',
            key
        )
        return content
    
    except frappe.exceptions.DoesNotExistError:
        return None