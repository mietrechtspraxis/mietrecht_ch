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
def get_details(name=None):
    if len(name) < MINIMUM_CHARACTER:
        raise BadRequestException(f'The search term must have at least {MINIMUM_CHARACTER} characters.')
    
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
            ["title_de", "=", name],
        ]
        
    ) 
    
    if len(result_data) != 0 and result_data != '':
        new_dict = result_data[0]
    
        mp_edition = str(new_dict.mp_edition)
        mp_edition_start_page = str(new_dict.mp_edition_start_page)
        
        concatenated_mp = f'{mp_edition}' + ' S. ' + f'{mp_edition_start_page}'
        new_dict.mp = concatenated_mp
        return new_dict
    
    raise BadRequestException("No data found for " + name)