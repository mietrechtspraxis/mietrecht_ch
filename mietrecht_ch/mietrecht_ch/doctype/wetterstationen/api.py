import frappe
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_all():
    locations  = execute_query("""SELECT `value` as `value`, `label` as `label`
                            FROM `tabWetterstationen` 
                            ;""")

    return locations