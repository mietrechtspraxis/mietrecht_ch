import frappe
import datetime
from frappe import _
from frappe.auth import LoginManager
from mietrecht_ch.models.jwt import JWTGenerator


@frappe.whitelist(allow_guest=True)
def auth(user, pwd, expires_in=3600, expire_on=None):

    try:
        login = LoginManager()
        login.user = user
        login.authenticate(user, pwd)
        login.post_login()
    except:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }
        return 
    
    user_role = __get_user_info__(user)
    
    generated_jwt = __generate_jwt__(user, user_role)
        
    response = frappe.response["message"] = {
        "success_key":1,
        "message":"Authentication success",
        "sid":frappe.session.sid,
        "jwt":generated_jwt,
    }
    
    # Return the current user session.
    return response

def __generate_jwt__(user, user_role):
    token = JWTGenerator('secret')
    expire_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {'user': user, 'role': user_role, 'exp': expire_time}
    generated_jwt = token.generate_token(payload)
    print(generated_jwt)
    return generated_jwt

def __get_user_info__(user):
    get_info_user = frappe.db.get_value('User', user, ['name', 'first_name','last_name', 'role_profile_name', 'api_key'], as_dict=1)
    user_role = get_info_user.role_profile_name
    return user_role

