import frappe
import jwt
import datetime

MP_WEB_USER_ROLE = "mp_web_user_abo"
MP_WEB_ADMIN_ROLE = "mp_web_admin"

JWT_HOURS_EXPIRY = 24

def failed_auth_response():
  clean_response()
  frappe.response["message"] = {
      "success": False,
      "message": "Not allowed",
  }

def success_auth_reponse(extra_info = None):
  clean_response()
  response = {
      "success": True,
  }

  if (extra_info is not None):
    response = {**response, **extra_info}

  frappe.response["message"] = response

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
  
  user_details.api_secret = decrypted_secret
  
  return user_details

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

def get_jwt(user_details, mp_roles):
  secret = "some_secret"

  payload = {
    'iss': 'mietrecht.ch',
    'sub': user_details.username,
    'aud': 'mietrecht.ch',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_HOURS_EXPIRY),
    'iat': datetime.datetime.utcnow(),
    'api_key': user_details.api_key,
    'api_secret': user_details.api_secret,
    'email': user_details.email,
    'first_name': user_details.first_name,
    'last_name': user_details.last_name,
    'mp_roles': mp_roles
  }

  token_bytes = jwt.encode(payload, secret, algorithm="HS256")

  token = token_bytes.decode('utf-8') 

  return token
