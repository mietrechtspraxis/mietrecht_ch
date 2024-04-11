import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _
from datetime import datetime
from frappe.config import get_modules_from_all_apps
from frappe.exceptions import DoesNotExistError


MESSAGE_ERROR = { 'created': False, 'cmsErrorKey' : 'SHOP_ERROR_BESTELLUNG' }
MP_ABO_ROLE = "mp_web_user_abo"

@frappe.whitelist(allow_guest=True)
def create_form_answer():
    try:
        request = __return_json_data__()

        if request is not None and len(request) != 0:
            if not __validate_fields__(request):
                return create_form_response(request)
        clean_response()
        return MESSAGE_ERROR
    except Exception as e:
        return "An error occurred: {0}".format(str(e))

def create_form_response(request):
    email = request.get('email')
    
    
    # Create doctype structure
    different_delivery_address, doc = __create_doctype_structure__(request)

    # Add delivery address to the doctype if different address is checked
    if different_delivery_address:
        __add_different_address_to_doctype__(request, doc)

    data = json.loads(request.get('data'))
    abo_data = data.get('abo')

    # Anlage Benutzer (User) bei Digitalen-Abo's
    if abo_data and abo_data.startswith(("PERI-ABO-", "PERI-3DAY%")):
        try:
            user = frappe.get_doc('User', email)
            __add_role_mp__(user)
        except DoesNotExistError:
            user = __create_base_user__(request)
            __add_role_mp__(user)
        except:
            clean_response()
            return MESSAGE_ERROR
        finally:
            clean_response()
        
    
    doc.insert(ignore_permissions=True)
    
    return { 'created': True, 'orderNumber': doc.name }

def __create_doctype_structure__(request):
    billing_address = request.get('billing_address', {})

    doc = frappe.new_doc('Antwort auf das Formular')
    doc.update({
        'gender': billing_address.get('gender'),
        'first_name': billing_address.get('first_name'),
        'last_name': billing_address.get('last_name'),
        'company': billing_address.get('company'),
        'additional_info': billing_address.get('additional_info'),
        'street': billing_address.get('street'),
        'po_box': billing_address.get('po_box'),
        'zip_and_city': billing_address.get('zip_and_city'),
        'email': request.get('email'),
        'type': request.get('type'),
        'data': json.dumps(json.loads(request.get('data')), indent=2),
        'remarks': request.get('remarks'),
        'different_delivery_address': request.get('different_delivery_address'),
    })

    return request.get('different_delivery_address'), doc

def __add_different_address_to_doctype__(request, doc):
    delivery_address = request.get('delivery_address')
    
    delivery_data = {
        'gender': delivery_address.get('gender'),
        'first_name': delivery_address.get('first_name'),
        'last_name': delivery_address.get('last_name'),
        'company': delivery_address.get('company'),
        'street': delivery_address.get('street'),
        'po_box': delivery_address.get('po_box'),
        'zip_and_city': delivery_address.get('zip_and_city'),
        'additional_info': delivery_address.get('additional_info'),
    }

    doc.update({
            'delivery_' + key: value for key, value in delivery_data.items()
        })
    
def __add_role_mp__(user):
    user.flags.ignore_permissions = True
    user.remove_roles()
        
    user.add_roles(MP_ABO_ROLE)
    user.save()

def __create_base_user__(request):  
    email = request.get('email')
    billing_address = request.get('billing_address', {})
    first_name = billing_address.get('first_name')
    last_name = billing_address.get('last_name')

    user = frappe.get_doc({
        "doctype":"User",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "user_type": "Website User"
        })


    user.flags.ignore_permissions = True
    user.flags.ignore_password_policy = True
    user.block_modules = __remove_modules_to_user__(request)
    user.insert()
    return user

def __generate_random_code__():
    return frappe.generate_hash(length=10)

def __remove_modules_to_user__(request):
    all_modules = get_modules_from_all_apps()
    blocked_modules = []
    date = datetime.now()
    random_code = __generate_random_code__()

    for index, module in enumerate(all_modules):
        blocked_modules.append(frappe.get_doc({
        "creation": date,
        "docstatus": 0,
        "doctype": "Block Module",
        "idx": index + 1 ,
        "modified": date,
        "modified_by": "Administrator",
        "module": module['module_name'],
        "name": random_code,
        "owner": "Administrator",
        "parent": request.get('email'),
        "parentfield": "block_modules",
        "parenttype": "User"
    }))

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
        clean_response()
        return billing_error

    # Validate delivery address
    delivery_error = __validate_address_fields__(delivery_address)
    if delivery_error:
        clean_response()
        return delivery_error

    return None

def __return_json_data__():
    content_type = frappe.get_request_header('Content-Type')
    if content_type != 'application/json':
        frappe.throw("Invalid content type. Expected application/json.", title="Bad Request")

    return json.loads(frappe.local.request.data.decode('utf-8'))

def clean_response():
  if '_server_messages' in frappe.response:
    del frappe.response['_server_messages']
  if ('exc_type' in frappe.response):
    del frappe.response["exc_type"]
