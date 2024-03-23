import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.utils.auth import MP_WEB_ADMIN_ROLE, MP_WEB_USER_ROLE
from frappe.model.document import Document
from datetime import datetime
import requests
import re

MINIMUM_CHARACTER = 4

@frappe.whitelist(allow_guest=True)
def search_decision_simple(term=None):
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
        },
        order_by=""
        # TODO: zuerst typ (aufsatz, entscheid, flash)
        # type bge dann alle anderen, dann 
        # chronologisch umgekehrt
    )
    
    
    return search_data

@frappe.whitelist(allow_guest=True)
def search_decision(term=None):
    '''
    v01
    v02 suche nach datum
    '''
    term = term.strip()
    if len(term) < MINIMUM_CHARACTER:
        raise BadRequestException(f'The search term must have at least {MINIMUM_CHARACTER} characters.')

    # Sanitize the input term to prevent SQL injection
    term = frappe.db.escape('%{}%'.format(term), percent=False)

    # Check if the term is a date in the format dd.mm.yyyy

    def term_is_date(term, formats=None):
        term = term[2:-2]

        if formats is None:
            formats = ['%d.%m.%Y','%Y-%m-%d']
        
        for date_format in formats:
            try:
                parsed_date = datetime.strptime(term, date_format)
                return parsed_date.strftime('%Y-%m-%d')  
            except ValueError:
                continue 
        return False  

    # Define the fields to be selected
    fields = [
        "`tabEntscheid`.`court`",
        "`tabEntscheid`.`type`", 
        "`tabEntscheid`.`title_de`",
        "`tabEntscheid`.`decision_date`",
        "`tabEntscheid`.`name`",
        "`tabEntscheid`.`author`",
        "`tabEntscheid`.`description_de`",
        "`tabEntscheid`.`decision_number`",
        "`tabEntscheid`.`article_new`",
        "`tabEntscheid`.`mp_edition`"
    ]

    # Define the filters
    filters = "(`tabEntscheid`.`type` IN ('Entscheid', 'Aufsatz', 'Flash'))"

    # Spezialfall Suche nach Datum
    decision_date = term_is_date(term)
    if decision_date:
        # Define the or_filters
        or_filters = """
            (`tabEntscheid`.`decision_date` = '{decision_date}')
        """.format(decision_date=decision_date)
    else:
        # Define the or_filters
        or_filters = """
            (`tabEntscheid`.`title_de` LIKE {term}
            OR `tabEntscheid`.`mp_edition` LIKE {term}
            OR `tabEntscheid`.`description_de` LIKE {term}
            OR `tabEntscheid`.`decision_number` LIKE {term}
            OR `tabEntscheid`.`official_collection` LIKE {term}
            OR `tabEntscheid`.`article_new` LIKE {term})
        """.format(term=term)

    # Define the order by clause with CASE statements
    order_by = """
        CASE
            WHEN `tabEntscheid`.`type` = 'Aufsatz' THEN 1
            WHEN `tabEntscheid`.`court` = 'BGE' THEN 2
            ELSE 3
        END,
        `tabEntscheid`.`decision_date` DESC
    """

    # Build the query
    query = """
        SELECT {fields}
        FROM `tabEntscheid`
        WHERE {filters}
        AND {or_filters}
        ORDER BY {order_by}
        LIMIT 200
    """.format(fields=', '.join(fields), filters=filters, or_filters=or_filters, order_by=order_by)

    # Execute the query
    search_data = frappe.db.sql(query, as_dict=True)

    # Get result count
    number_of_results = len(search_data)

    # Log the search term
    log_search_term(term,number_of_results)

    return search_data

def log_search_term(term,number_of_results):
    try:
        # Create a new SearchLog document
        search_log = frappe.get_doc({
            "doctype": "SearchLog",
            "search_term": term[2:-2],
            "result_count": number_of_results,
            "source": frappe.local.request_ip
        })
        search_log.insert(ignore_permissions=True)  # Use ignore_permissions=True if needed
        frappe.db.commit()  # Ensure the transaction is committed
    except Exception as e:
        frappe.log_error(title="Failed to log search term", message=str(e))

@frappe.whitelist(allow_guest=True)
def get_details(name=None):
    frappe.only_for((MP_WEB_USER_ROLE, MP_WEB_ADMIN_ROLE))
    result_data = frappe.get_all('Entscheid',
        fields=[
            "type",
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
            "mp_flash",
            "mp_flash_summary",
            "mp_flash_text",
            "mp_flash_filename",
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
    
@frappe.whitelist(allow_guest=True)
def serve_file(file_name,download=False):
    frappe.only_for((MP_WEB_USER_ROLE, MP_WEB_ADMIN_ROLE))

    def sanitize_filename(filename):
        """
        Sanitizes the filename by removing potentially dangerous characters
        and sequences. This function is conservative and designed to ensure
        safety and compatibility across different systems.
        """
        # Remove directory navigation attempts
        filename = re.sub(r'\.\./|\.\.\\', '', filename)
        
        # Remove characters that are not letters, numbers, underscores, hyphens, or periods.
        filename = re.sub(r'[^\w\-\.]', '', filename)
        filename = filename[:255]
        
        return filename

    frontend_settings = frappe.get_doc("frontend settings")
    file_path_pdf = frontend_settings.file_path_pdf

    file_name = sanitize_filename(file_name)

    file_url = file_path_pdf + file_name

    try:
        # Fetch the file from the remote server
        response = requests.get(file_url, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Set the filename and content type in the response
            file_name = file_url.split('/')[-1]
            frappe.local.response.filename = file_name
            frappe.local.response.filecontent = response.content
            #frappe.local.response.headers["Content-Disposition"] = 'inline; filename="{0}"'.format(file_name)

            if download == False:
                frappe.local.response.type = 'pdf' #"download" 
            else: 
                frappe.local.response.type = "download" 
        else:
            frappe.local.response.http_status_code = 404
            return {'error': 'File not found on remote server'}
    except Exception as e:
        frappe.local.response.http_status_code = 500
        return {'error': str(e)} 
    
