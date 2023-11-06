import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _

@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_response_form():
    request = is_post_method()

    if request is not None and len(request) != 0:

        if not __validate_fields__(request):
           return __insert_new_document__(request)
            
        return __validate_fields__(request)
        
        
    return BadRequestException('The form cannot be empty.')
    

def __insert_new_document__(request):
    first_name = request.get('first_name')
    last_name = request.get('last_name')
    firma = request.get('firma')
    street = request.get('street')
    zip_code = request.get('zip_code')
    company_number = request.get('company_number')
    
    doc = frappe.new_doc('Antwort auf das Formular')
    doc.first_name = first_name
    doc.last_name = last_name
    doc.firma = firma
    doc.zip_code = zip_code
    doc.street = street
    doc.company_number = company_number
    doc.insert(ignore_permissions=True)
    
    # frappe.sendmail(
    #     ["david.planchon@liip.ch"],
    #     message="## hello, *bro*",
    #     attachments=[{"file_url": "/files/hello.png"}],
    #     as_markdown=True
    #     )
    
    # start creating the new_doc based on received data
    return {'response': 'Die Bestellung eines Kursprogramms wurde erfolgreich gesendet.'}
    
def __validate_fields__(request):
    errors = []
    for k in [request]:
        first_name = k['first_name']
        last_name = k['last_name']
        firma = k['firma']
        street = k['street']
        company_number = k['company_number']
        zip_code = k['zip_code']
        
        if (first_name == "" and len(first_name) == 0 or last_name == "" and len(last_name) == 0) and firma == "" and len(firma) == 0 :
            errors.append({'error' : 'Please add either a First Name and Last Name or a Firma value.'})
            
        if (street == "" and len(street) == 0 or zip_code == "" and len(zip_code) == 0) and (company_number == "" and len(company_number) == 0):  
            errors.append({'error' : 'Please add either a Street and zip code or a valid Company Number.'})
    
    if errors:
        return errors

def is_post_method():
    if frappe.request.method == "POST":
        request_data = frappe.local.request.data
        request_data_str = request_data.decode('utf-8')

        request_data = json.loads(request_data_str)

        return request_data