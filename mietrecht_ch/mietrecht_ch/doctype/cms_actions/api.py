import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def get_cms_actions(action_group_key):
    
    if len(action_group_key) == 0:
        raise BadRequestException('Name cannot be empty.')
    
    
    test_sql = frappe.db.sql(""" 
        SELECT 
        a.cms_key, a.title, a.url, a.description, a.is_internal, f.file_url, file_name
        FROM `tabCMS Actions` AS a
        LEFT JOIN tabFile AS f ON a.file=f.name
    """)
    return test_sql
    
    
