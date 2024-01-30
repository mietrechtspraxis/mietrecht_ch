import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def get_all():
    get_all = frappe.get_all('Kurse und Seminare',
    fields=[
        "title",
        "iframe_uri",
        "display_order",
        "name"
    ], 
    order_by="display_order ASC"
    
)
    return get_all

@frappe.whitelist(allow_guest=True)
def get_by_name(name):
    
    if len(name) == 0 or name == '':
        raise BadRequestException('Name cannot be empty.')
    
    
    get_result_by_name = frappe.get_all('Kurse und Seminare',
    fields=[
        "title",
        "iframe_uri",
        "display_order",
        "name"
    ],
       filters=[
            ['name', '=', name],
    ],
    order_by="display_order ASC"
    
)
    if len(get_result_by_name) != 0 and get_result_by_name is not None:
        result = get_result_by_name[0]
        return result
    return None
