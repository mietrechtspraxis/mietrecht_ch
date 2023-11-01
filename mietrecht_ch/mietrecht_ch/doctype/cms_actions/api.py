import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def get_editable_actions(action_group_key):
    get_action_information = frappe.get_doc('CMS Action', action_group_key, )