import frappe
from frappe import _
from frappe.auth import LoginManager
import json

@frappe.whitelist(allow_guest=True)
def auth(user, pwd):
    try:
        login = LoginManager()
        login.authenticate(user=user, pwd=pwd)
        login.post_login()
        frappe.clear_messages()
    except:
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }
        return 
    
    user_roles = frappe.get_roles(frappe.session.user)
    mp_roles = [role for role in user_roles if role.startswith("mp_web")]
    frappe.local.cookie_manager.set_cookie("mp_roles", json.dumps(mp_roles))
    del frappe.local.response["home_page"]
    del frappe.local.response["full_name"]
    
    response = frappe.response["message"] = {
        "success_key":1,
        "message":"Authentication success",
    }
    
    return response

@frappe.whitelist(allow_guest=True)
def logout():
    LoginManager().logout()
    frappe.local.response["message"]= {
        'success_key': 1,
        "message":"Logout success",
    }