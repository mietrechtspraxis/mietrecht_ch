import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _

@frappe.whitelist(allow_guest=True, methods=['POST'])
def create_response_form():
    request = is_post_method()

    if request is not None and len(request) != 0:
        
        try:
            if not __validate_fields__(request):
                return __insert_new_document__(request)
            
            return __validate_fields__(request)
        except Exception as e:
            return f"An error occurred: {str(e)}"
            
        
        
    return BadRequestException('The form cannot be empty.')
    

def __insert_new_document__(request):
    genre = request.get('genre')
    first_name = request.get('first_name')
    last_name = request.get('last_name')
    company = request.get('company')
    street = request.get('street')
    company_number = request.get('company_number')
    zip_code = request.get('zip_code')
    address_complement = request.get('address_complement')
    email = request.get('email')
    annotation = request.get('annotation')
    additional_data = request.get('additional_data')
    type_form = request.get('type')
    firma = request.get('firma')
    
    doc = frappe.new_doc('Antwort auf das Formular')
    doc.first_name = first_name
    doc.last_name = last_name
    doc.firma = firma
    doc.zip_code = zip_code
    doc.street = street
    doc.company_number = company_number
    doc.type = type_form
    doc.email = email
    doc.genre = genre
    doc.annotation = annotation
    doc.address_complement = address_complement
    doc.additional_data = additional_data
    doc.company = company
    doc.insert(ignore_permissions=True)
    
    # start creating the new_doc based on received data
    return {'success': True}
    
def __validate_fields__(request):
    errors = []
    for k in [request]:
        first_name = k['first_name']
        last_name = k['last_name']
        firma = k['firma']
        street = k['street']
        company_number = k['company_number']
        zip_code = k['zip_code']
        
        if (first_name == "" or last_name == "" ) and firma == "":
            errors.append({'error' : 'Please add either a First Name and Last Name or a Firma value.'})
            
        if (street == "" or zip_code == "") and (company_number == ""):  
            errors.append({'error' : 'Please add either a Street and zip code or a valid Company Number.'})
    
    if errors:
        return errors

def is_post_method():
    if frappe.request.method == "POST":
        if frappe.get_request_header('Content-Type') != 'application/json':
            frappe.throw("Invalid content type. Expected application/json.", title="Bad Request")
    
    request_data = frappe.local.request.data
    request_data_str = request_data.decode('utf-8')

    request_data = json.loads(request_data_str)

    return request_data
