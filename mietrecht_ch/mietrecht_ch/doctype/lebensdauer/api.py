import frappe

@frappe.whitelist(allow_guest=True)
def get_all_by_group(groupId):
    return { 'params': {'groupId':groupId}}


@frappe.whitelist(allow_guest=True)
def get_all_by_keyword(keyword):
    return { 'params': {'keyword':keyword}}
