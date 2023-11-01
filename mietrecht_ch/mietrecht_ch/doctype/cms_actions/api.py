import json
import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from pprint import pprint
from urllib.parse import urlparse

from mietrecht_ch.utils.hostUtils import get_website_url

@frappe.whitelist(allow_guest=True)
def get_cms_actions(action_group_key):
    
    if len(action_group_key) == 0:
        raise BadRequestException('Name cannot be empty.')
    
    
    db_actions = frappe.db.sql(""" 
        SELECT a.cms_key, a.title, a.url, a.description, a.is_internal, f.file_url
        FROM `tabCMS Actions` AS a
        LEFT JOIN tabFile AS f ON a.file=f.name
    """)

    actions = []

    site_url = get_website_url()

    for db_action in db_actions:
        action = {
            'key': db_action[0],
            'title': db_action[1],
            'url': db_action[2],
            'description': db_action[3],
            'isInternal': db_action[4],
            'fileUrl': f"{site_url}{db_action[5]}" if db_action[5] is not None else None,
        }
        actions.append(action)

    return actions
    
    
