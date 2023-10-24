import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def healthcheck():
    answer = {
        "code": 200,
    }
    return answer


@frappe.whitelist(allow_guest=True)
def search_decision(searchTerm=None):
    
    if len(searchTerm) < 4:
        raise BadRequestException('The search term must have at least 4 characters.')
    
    searchData = frappe.get_all('Entscheide',
        filters={
            ""
        })
    
    print(searchData)