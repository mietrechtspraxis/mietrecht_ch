import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.utils.auth import MP_WEB_ADMIN_ROLE, MP_WEB_USER_ROLE

MINIMUM_CHARACTER = 4

@frappe.whitelist(allow_guest=True)
def search_decision(term=None):

    if len(term) < MINIMUM_CHARACTER:
        raise BadRequestException(f'The search term must have at least {MINIMUM_CHARACTER} characters.')
    
    escaped_searched_term =  ["like", f"%{term}%"]  
  
    search_data = frappe.get_all('Entscheid',
        fields={
            "court",
            "title_de",
            "decision_date",
            "name",
            "description_de",
            "decision_number",
            "article_new"
        },
        filters={
            'type': ['in', 'Entscheid', "Aufsatz"],
        },
        or_filters={
            'title_de': escaped_searched_term,
            'description_de': escaped_searched_term,
            'decision_number': escaped_searched_term,
            'official_collection': escaped_searched_term,
            'article_new': escaped_searched_term
        }
    )
    
    
    return search_data

@frappe.whitelist(allow_guest=True)
def get_details(name=None):
    frappe.only_for((MP_WEB_USER_ROLE, MP_WEB_ADMIN_ROLE))
    result_data = frappe.get_all('Entscheid',
        fields=[
            "mp_edition",
            "mp_edition_start_page",
            "id_old", #legacy
            "title_de",
            "decision_date",
            "court",
            "description_de",
            "title_fr",
            "description_fr",
            "article_new",
            "decision_number",
            "official_collection",
            "authority",
            "ref_die_praxis",
            "ref_semaine_judiciaire", 
            "ref_droit_du_bail", 
            "ref_cahiers_du_bail",
            "ref_mietrecht_aktuell",
            "mp_filename",
            "author",
            "author_info_de"
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
    