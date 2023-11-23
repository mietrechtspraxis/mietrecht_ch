import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _
from datetime import datetime
from frappe.config import get_modules_from_all_apps
import secrets
import string


MESSAGE_ERROR = { 'created': False, 'cmsErrorKey' : 'SHOP_ERROR_BESTELLUNG' }
MP_ABO_ROLE = "mp_web_user_abo"

@frappe.whitelist(allow_guest=True, methods=['POST'])
def create_form_answer():
    try:
        request = __return_json_data__()

        if request is not None and len(request) != 0:
            if not __validate_fields__(request):
                return create_form_response(request)
            return MESSAGE_ERROR
    except Exception as e:
        return f"An error occurred: {str(e)}"
        
    return BadRequestException('The form cannot be empty.')
    
def __get_address_data__(request):
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
    # Create doctype structure
    first_name, last_name, email, different_delivery_address, doc = __create_doctype_structure__(request)

    # Add delivery address to the doctype if different address is checked
    if different_delivery_address:
        __add_different_address_to_doctype__(request, doc)

    data = json.loads(request.get('data'))
    abo_data = data.get('abo')

    if abo_data and abo_data.startswith(("PERI-ABO-", "PERI-3DAY%", "Probe-Abo")):
        try:
            __create_base_user__(first_name, last_name, email)   
            __add_role_mp__(email)
            return {'userCreated': True}
        except:
            return MESSAGE_ERROR
    
    doc.insert(ignore_permissions=True)

    return { 'created': True, 'orderNumber': doc.name }

def __create_doctype_structure__(request):
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
    
    return first_name,last_name,email,different_delivery_address,doc

def __add_different_address_to_doctype__(request, doc):
    delivery_data = __get_address_data__(request)
    doc.update({
            'delivery_' + key: value for key, value in delivery_data.items()
        })

def __add_role_mp__(email):
    user_modification = frappe.get_doc('User', email)
    user_modification.flags.ignore_permissions = True
    user_modification.remove_roles()
        
    user_modification.add_roles(MP_ABO_ROLE)
    user_modification.save()
    return user_modification

def __create_base_user__(first_name, last_name, email):
    user = frappe.get_doc({
            "doctype":"User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "user_type": "Website User"
            })
    
    user.flags.ignore_permissions = True
    user.flags.ignore_password_policy = True
    user.block_modules = __blocked_modules__(email)
    user.insert()

def __generate_random_code__(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def __remove_modules_to_user__(index, module, date, email):
    random_code = __generate_random_code__()
    module_doctype = frappe.get_doc({
        "creation": date,
        "docstatus": 0,
        "doctype": "Block Module",
        "idx": index + 1,
        "modified": date,
        "modified_by": "Administrator",
        "module": module['module_name'],
        "name": random_code,
        "owner": "Administrator",
        "parent": email,
        "parentfield": "block_modules",
        "parenttype": "User"
    })
    return module_doctype

def __blocked_modules__(email):
    all_modules = get_modules_from_all_apps()
    blocked_modules = []
    date = datetime.now()

    for index, module in enumerate(all_modules):
        module_doctype = __remove_modules_to_user__(index, module, date, email)
        blocked_modules.append(module_doctype)

    return blocked_modules

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

def __return_json_data__():
    if frappe.get_request_header('Content-Type') != 'application/json':
        frappe.throw("Invalid content type. Expected application/json.", title="Bad Request")
        
    request_data_str = frappe.local.request.data.decode('utf-8')

    return json.loads(request_data_str)
