from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.auth import LoginManager
import json
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def healthcheck():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    answer = {
        "code": 200,
        "message": "Bor to be Alive",
        "timeStamp": dt_string,
        "version": "0.0.5",
        "branch": "ebook"
        }
    return answer


@frappe.whitelist(allow_guest=True)
def login(user, pwd):
    try:
        login = LoginManager()
        login.authenticate(user=user, pwd=pwd)
        login.post_login()
        frappe.clear_messages()
    except:
        frappe.local.response["message"] = {
            "success": False,
            "message": "Authentication Error!"
        }
        return 
    
    user_roles = frappe.get_roles(frappe.session.user)
    
    mp_roles = [role for role in user_roles if role.startswith("mp_web")]
    
    frappe.local.cookie_manager.set_cookie("mp_roles", json.dumps(mp_roles))
    del frappe.local.response["home_page"]
    del frappe.local.response["full_name"]
    
    response = frappe.response["message"] = {
        "success": True,
        "message": "Authentication success",
    }
    
    return response

@frappe.whitelist(allow_guest=True)
def logout():
    LoginManager().logout()
    frappe.local.response["message"]= {
        'success': True,
        "message": "Logout success",
    }



