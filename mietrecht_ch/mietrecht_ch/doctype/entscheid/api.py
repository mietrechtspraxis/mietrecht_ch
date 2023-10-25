import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

MINIMUM_CHARACTER = 4

@frappe.whitelist(allow_guest=True)
def search_decision(search=None):

    print(search)
    if len(search) < MINIMUM_CHARACTER:
        raise BadRequestException(f'The search term must have at least {MINIMUM_CHARACTER} characters.')
    
    escaped_searched_term =  ["like", f"%{search}%"]  
  
    search_data = frappe.get_all('Entscheid',
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
    
    
    return search_data

@frappe.whitelist(allow_guest=True)
def get_details(name=None):
    
    result_data = frappe.get_all('Entscheid',
        fields=[
            "title_de",
            "decision_date",
            "court",
            "decision_number",
            "official_collection",
            "description_de",
            "mp_edition",
            "mp_edition_start_page"
            
        ],
        filters=[
            ["name", "=", name],
        ]
        
    ) 
    
    if len(result_data) != 0 and result_data is not None:
        new_dict = result_data[0]
        mp_edition = new_dict.mp_edition
        mp_edition_start_page = new_dict.mp_edition_start_page
        
        new_dict.mp = f"{mp_edition} S. {mp_edition_start_page}"
        return new_dict
    
    return None
    