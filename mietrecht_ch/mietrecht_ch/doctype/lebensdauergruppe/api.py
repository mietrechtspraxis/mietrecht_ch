import frappe
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_all():
    return frappe.get_all('LebensdauerGruppe', fields=['value', 'label'])