import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

MINIMUM_CHARACTER = 4

@frappe.whitelist(allow_guest=True)
def healthcheck():
    answer = {
        "code": 200,
    }
    return answer


@frappe.whitelist(allow_guest=True)
def search_decision(search=None):
    if len(search) < MINIMUM_CHARACTER:
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
    
    if len(name) < MINIMUM_CHARACTER:
        raise BadRequestException('The search term must have at least 4 characters.')
    
    escaped_name =  ["like", f"%{name}%"]
    
    
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
        },or_filters={
            'name': escaped_name,
        }
        
    ) 
    
    if len(searchData) != 0 and searchData != '':
        mp_edition = searchData[0].mp_edition
        mp_edition_start_page = searchData[0].mp_edition_start_page
        
        concatenated_mp = _mp_concatenation_(mp_edition, mp_edition_start_page)
        searchData[0].mp = concatenated_mp
        return searchData
    
    raise BadRequestException("No data found for " + name)


def _mp_concatenation_(value1, value2):
    return str(value1) + ' S. ' + str(value2)