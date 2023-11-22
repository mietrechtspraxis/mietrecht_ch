import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _

MESSAGE_ERROR = { 'created': False, 'cmsErrorKey' : 'SHOP_ERROR_BESTELLUNG' }

@frappe.whitelist(allow_guest=True, methods=['POST'])
def create_response_form():
    try:
        request = return_json_data()

        if request is not None and len(request) != 0:
            if not __validate_fields__(request):
                return create_form_response(request)
            return MESSAGE_ERROR
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
        'po_box': delivery_address.get('po_box'),
        'zip_and_city': delivery_address.get('zip_and_city'),
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
    po_box = billing_address.get('po_box')
    zip_and_city = billing_address.get('zip_and_city')
    
    email = request.get('email')
    remarks = request.get('remarks')
    type_form = request.get('type')
    data = json.dumps(json.loads(request.get('data')), indent=2)
    different_delivery_address = request.get('different_delivery_address')

    # Create main form response document
    doc = frappe.new_doc('Antwort auf das Formular')
    doc.update({
        'gender': gender,
        'first_name': first_name,
        'last_name': last_name,
        'company': firma,
        'additional_info': additional_info,
        'street': street,
        'po_box': po_box,
        'zip_and_city': zip_and_city,
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

    return { 'created': True, 'orderNumber': doc.name }

def __validate_address_fields__(address):
    last_name = address.get('last_name', '')
    company = address.get('company', '')
    street = address.get('street', '')
    po_box = address.get('po_box', '')
    zip_and_city = address.get('zip_and_city', '')

    if last_name == "" and company == "":
        return MESSAGE_ERROR

    if street == "" and po_box == "":
        return MESSAGE_ERROR
    
    if zip_and_city == "":
        return MESSAGE_ERROR

    # Validation succeeded
    return None

def __validate_fields__(request):
    billing_address = request.get('billing_address', {})
    delivery_address = request.get('delivery_address', {})

    # Validate billing address
    billing_error = __validate_address_fields__(billing_address)
    if billing_error:
        return billing_error

    # Validate delivery address
    delivery_error = __validate_address_fields__(delivery_address)
    if delivery_error:
        return delivery_error

    return None

def return_json_data():
    if frappe.get_request_header('Content-Type') != 'application/json':
        frappe.throw("Invalid content type. Expected application/json.", title="Bad Request")
        
    request_data_str = frappe.local.request.data.decode('utf-8')

    return json.loads(request_data_str)
