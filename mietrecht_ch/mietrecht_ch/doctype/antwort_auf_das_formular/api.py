import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _

@frappe.whitelist(allow_guest=True, methods=['POST'])
def create_response_form():
    request = return_json_data()

    if request is not None and len(request) != 0:
        try:
            if not __validate_fields__(request):
                return create_form_response(request)
            return __validate_fields__(request)
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    return BadRequestException('The form cannot be empty.')
    
def get_address_data(request, address_key):
    delivery_address = request.get('delivery_address')
    
    return {
        'gender': delivery_address.get('gender'),
        'first_name': delivery_address.get('first_name'),
        'last_name': delivery_address.get('last_name'),
        'firma': delivery_address.get('company'),
        'street': delivery_address.get('street'),
        'company': delivery_address.get('po_box'),
        'zip_code': delivery_address.get('zip_and_city'),
        'additional_info': delivery_address.get('additional_info'),
    }

    
def create_form_response(request):
    # Main form data
    billing_address = request.get('billing_address')
    gender = billing_address.get('gender')
    first_name = billing_address.get('first_name')
    last_name = billing_address.get('last_name')
    firma = billing_address.get('company')
    additional_info = billing_address.get('additional_info')
    street = billing_address.get('street')
    company_number = billing_address.get('po_box')
    zip_code = billing_address.get('zip_and_city')
    
    email = request.get('email')
    remarks = request.get('remarks')
    type_form = request.get('type')
    data = json.dumps(request.get('products'))
    different_delivery_address = request.get('different_delivery_address')

    # Create main form response document
    doc = frappe.new_doc('Antwort auf das Formular')
    doc.update({
        'gender': gender,
        'first_name': first_name,
        'last_name': last_name,
        'company': company_number,
        'additional_info': additional_info,
        'street': street,
        'company_number': firma,
        'zip_code': zip_code,
        'email': email,
        'type': type_form,
        'data': data,
        'remarks': remarks,
        'different_delivery_address': different_delivery_address,
    })

    # Create or update delivery address
    if different_delivery_address:
        delivery_data = get_address_data(request, 'delivery_address')
        doc.update({
            'delivery_' + key: value for key, value in delivery_data.items()
        })

    doc.insert(ignore_permissions=True)

    return {'success': True}
    
def __validate_fields__(request):
    errors = []
    for k in [request]:
        billing_address = k['billing_address']
        first_name = billing_address['first_name']
        last_name = billing_address['last_name']
        firma = billing_address['po_box']
        street = billing_address['street']
        company_number = billing_address['po_box']
        zip_code = billing_address['zip_and_city']
        
        if (first_name == "" or last_name == "" ) and firma == "":
            errors.append({'error' : 'Please add either a First Name and Last Name or a Firma value.'})
            
        if (street == "" or zip_code == "") and (company_number == None):  
            errors.append({'error' : 'Please add either a Street and zip code or a valid Company Number.'})
    
    if errors:
        return errors

def return_json_data():
    if frappe.get_request_header('Content-Type') != 'application/json':
        frappe.throw("Invalid content type. Expected application/json.", title="Bad Request")
        
    request_data_str = frappe.local.request.data.decode('utf-8')

    return json.loads(request_data_str)
