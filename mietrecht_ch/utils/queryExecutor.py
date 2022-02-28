import frappe
from pymysql import InternalError

log = frappe.logger("mietrecht.api")

def execute_query(query: str):
    result = None
    try:
        result  = frappe.db.sql(query, as_dict=True)
    except InternalError:
       log.error('Heizgradtagzahlen Request Error', exc_info=True)

    return result
