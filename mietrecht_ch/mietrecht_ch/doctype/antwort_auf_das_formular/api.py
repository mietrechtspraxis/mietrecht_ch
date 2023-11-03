import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _

@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_response_form():
    request = is_post_method()
    
    if request is not None and len(request) != 0:   
        first_name = request.get('first_name')
        last_name = request.get('last_name')
        email = request.get('email')
        _type = request.get('type')
        
        required_fields = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            '_type': _type    
         }
        
        __is_not_empty__(required_fields)
        
        doc = frappe.new_doc('Antwort auf das Formular')
        doc.first_name = first_name
        doc.last_name = last_name
        doc.email = email
        doc.email = _type
        doc.insert(ignore_permissions=True)
        
        # start creating the new_doc based on received data
        return 'all good'
    return BadRequestException('The form cannot be empty.')
    
    [
        {
            "genre": "String(dropdown)" - "Frau" | "Herr",
            "first_name": "String",
            "last_name": "String",
            "company": "String",
            "street": "String",
            "company_number": "Interger",
            "zip_code": "String",
            "address_complement": "String",
            "email": "String",
            "annotation": "String",
            "additional_data": "String",
            "type": "String(dropdown)" - "Bestellformular “Kurs- und Seminarprogramm”" | "Kontakt" | "Andere" 
        }   
    ]
    
def  __is_not_empty__(fields):
    errors = []    
    for k, v in fields.items():
        if v is "" and len(v) == 0:
            errors.append({ k : f'{k} cannot be empty.'})

    if errors:
        return errors

def is_post_method():
    if frappe.request.method == "POST":
        request_data = frappe.local.request.data
        request_data_str = request_data.decode('utf-8')

        request_data = json.loads(request_data_str)

        # Access and process the data from the request body
        # data_value = request_data.get("key")
        return request_data