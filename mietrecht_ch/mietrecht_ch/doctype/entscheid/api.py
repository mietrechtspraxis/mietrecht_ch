import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def healthcheck():
    answer = {
        "code": 200,
    }
    return answer


@frappe.whitelist(allow_guest=True)
def search_decision(searchTerm):
    
    if len(searchTerm) < 4:
        raise BadRequestException('The search term must have at least 4 characters.')
    
    searchData = frappe.get_all('Entscheid',
        fields={
            "description_de",
            "title_de",
            "decision_number",
            "official_collection"
        },
        filters={
            'type': ['in', 'Entscheid', "Aufsatz"],
            'title_de': ["like", "%{}%".format(searchTerm)]
        })
    
    return searchData