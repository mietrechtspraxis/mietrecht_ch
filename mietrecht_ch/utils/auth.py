import frappe
from frappe.auth import LoginManager

MP_WEB_USER_ROLE = "mp_web_user_abo"
MP_WEB_ADMIN_ROLE = "mp_web_admin"

def failed_auth_response():
  clean_response()
  frappe.response["message"] = {
      "success": False,
      "message": "Not allowed",
  }

def success_auth_reponse(message = None):
  clean_response()
  frappe.response["message"] = {
      "success": True,
      "message": message if message is not None else "Authentication success",
  }

def get_mp_roles(user):
  user_roles = frappe.get_roles(user)
       
  mp_roles = [role for role in user_roles if role.startswith("mp_web")]

  if len(mp_roles) == 0:
    raise Exception('No mp roles for this user')
  
  return mp_roles
  
def generate_api_keys(user):
  user_details = frappe.get_doc("User", user)
  api_secret = frappe.generate_hash(length=15)

	# if api key is not set generate api key
  if not user_details.api_key:
    api_key = frappe.generate_hash(length=15)
    user_details.api_key = api_key
  user_details.api_secret = api_secret
  user_details.save()


  decrypted_secret = frappe.utils.password.get_decrypted_password("User",
			user_details.name, fieldname='api_secret')
  
  print(f"Returning")
  return { 'api_key': user_details.api_key, 'api_secret': decrypted_secret}

def remove_api_key(user):
  user_details = frappe.get_doc("User", user)
  user_details.api_key = None
  user_details.api_secret = None
  user_details.save()

def clean_response():
  if ('home_page' in frappe.local.response):
    del frappe.local.response["home_page"]
  if ('full_name' in frappe.local.response):
    del frappe.local.response["full_name"]

def set_jwt_in_response(authentication_info, mp_roles):
  frappe.local.response["token"] = authentication_info
  frappe.local.response["roles"] = mp_roles
