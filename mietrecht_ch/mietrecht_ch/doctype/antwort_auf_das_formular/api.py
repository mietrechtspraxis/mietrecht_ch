import frappe
import json
from frappe import _

@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_response_form():
    if frappe.request.method == "POST":
        request_data = frappe.local.request.data
        request_data_str = request_data.decode('utf-8')

        # Parse the string as JSON
        request_data = json.loads(request_data_str)

        # Access and process the data from the request body
        # data_value = request_data.get("key")
        return request_data
      
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
    pass