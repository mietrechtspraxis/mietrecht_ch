import frappe
from frappe.core.doctype.user.user import sign_up
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import json
from frappe import _

MESSAGE_ERROR = { 'created': False, 'cmsErrorKey' : 'SHOP_ERROR_BESTELLUNG' }

@frappe.whitelist(allow_guest=True, methods=['POST'])
def create_form_answer():
    try:
        request = return_json_data()

        if request is not None and len(request) != 0:
            if not __validate_fields__(request):
                return create_form_response(request)
            return MESSAGE_ERROR
    except Exception as e:
        return f"An error occurred: {str(e)}"
        
    return BadRequestException('The form cannot be empty.')
    
def get_address_data(request):
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
        delivery_data = get_address_data(request)
        doc.update({
            'delivery_' + key: value for key, value in delivery_data.items()
        })

    data = json.loads(request.get('data'))
    abo_data = data.get('abo')
    full_name = f"{first_name + ' ' + last_name}"

    if abo_data == "PERI-ABO-%" or abo_data == "PERI-3DAY%" or abo_data == "Probe-Abo":
        # User creation account
        # sign_up(email, full_name, None)

        # upadte_sql = """
        #     UPDATE `tabModule Def` as md
        #     INNER JOIN `tabUser` as u ON u.email = "benoit.potty@liip.ch"
        #     SET u.enabled = 0
        #     WHERE u.enabled = 1
        #      """

        
        
        # result = frappe.db.sql(upadte_sql, as_dict=True)
        # return

        module_name = 'Accounts'

            # Fetch the user
        user = frappe.get_doc({
            "doctype":"User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "user_type": "Website User"
            })
            # Remove the module permission for the specified module
        modules = frappe.get_all("Module Def", fields=[])
        
        return modules
        # Print module information
        for module in modules:
            print(f"Module Name: {module.module_name}, Label: {module.label}")
        user.flags.ignore_permissions = True
        return user
        user.save()
        return

        # Remove the module from the roles assigned to the user
        for role in user_doc.get("roles"):
            role_doc = frappe.get_doc("Role", role.role)
            if module_name in role_doc.get("module_def_whitelist"):
                return True
                role_doc.remove("module_def_whitelist", {"module_def": module_name})
                role_doc.save()
                print(role_doc)

        # Clear cache to apply changes
        frappe.clear_cache()
        return
        # update_query = """
        #     UPDATE `tabModule Def`
        #     SET enabled = '0'
        #     WHERE email IN (SELECT * FROM `tabUser` WHERE email = 'benoit.potty@liip.ch');
        # """
        # result = frappe.db.sql(update_query, as_dict=True)
        # return result

        user = frappe.get_doc({
        "doctype":"User",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "user_type": "Website User"
		})


        
        user.flags.ignore_permissions = True
        user.flags.ignore_password_policy = True
        user.insert()
    

        user_modification = frappe.get_doc('User', email)
        user_modification.flags.ignore_permissions = True
        user_modification.remove_roles()
        user_modification.add_roles('mp_web_user_abo')
        return user_modification.save()
        
    

        
        
        
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
