import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

from mietrecht_ch.utils.hostUtils import get_website_url

@frappe.whitelist(allow_guest=True)
def get_cms_actions(action_group_key):
    
    if len(action_group_key) == 0:
        raise BadRequestException('Name cannot be empty.')
    
    
    db_actions = frappe.db.sql(""" 
        SELECT a.cms_key, a.title, a.url, a.description, a.is_internal ,f.file_url, a.file_attachment, a.file_url, a.weighting
        FROM `tabCMS Actions` AS a
        LEFT JOIN tabFile AS f ON a.file=f.name
        WHERE a.cms_key = %(key)s
        ORDER BY a.weighting ASC
    """, values={'key': action_group_key})

    actions = []

    site_url = get_website_url()

    for db_action in db_actions:
        action = {
            'key': db_action[0],
            'title': db_action[1],
            'url': db_action[2],
            'description': db_action[3],
            'isInternal': True if db_action[4] == 1 else False,
            'attachment': f"{site_url}{db_action[6]}" if db_action[6] is not None else None,
            'fileUrl': db_action[7],
            
        }
        actions.append(action)

    return actions
    
    
