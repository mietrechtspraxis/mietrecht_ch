import frappe

@frappe.whitelist(allow_guest=True)
def get_response_form_data():
    pass