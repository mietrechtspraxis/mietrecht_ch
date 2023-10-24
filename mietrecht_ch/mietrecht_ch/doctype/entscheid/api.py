import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def healthcheck():
    answer = {
        "code": 200,
    }
    return answer


@frappe.whitelist(allow_guest=True)
def search_decision(search=None):
    if search and len(search) < 4:
        raise BadRequestException('The search term must have at least 4 characters.')
    
    escaped_searched_term =  ["like", f"%{search}%"]  
  
    searchData = frappe.get_all('Entscheid',
        fields={
            "court",
            "title_de",
            "decision_date",
            "name",
            "description_de",
            "decision_number",
        },
        filters={
            'type': ['in', 'Entscheid', "Aufsatz"],
        },
        or_filters={
            'title_de': escaped_searched_term,
            'description_de': escaped_searched_term,
            'decision_number': escaped_searched_term,
            'official_collection': escaped_searched_term
        }
    )
    
    
    return searchData

@frappe.whitelist(allow_guest=True)
def search_detailed(name=None):
    if name and len(name) < 4:
        raise BadRequestException('The search term must have at least 4 characters.')
    
    searchData = frappe.get_all('Entscheid',
        fields={
            "title_de",
            "decision_date",
            "court",
            "decision_number",
            "official_collection",
            "description_de",
            "mp_edition",
            "mp_edition_start_page"
            
        },
        filters={
            'type': ['in', 'Entscheid', "Aufsatz"],
        }
    )
    
    
    return searchData