from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.auth import LoginManager
import datetime
from mietrecht_ch.utils.auth import *

@frappe.whitelist(allow_guest=True)
def healthcheck():
    now = datetime.datetime.utcnow()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    answer = {
        "code": 200,
        "message": "Born to be Alive",
        "timeStamp": dt_string,
        "version": "0.0.9",
        }
    return answer


# @frappe.whitelist(allow_guest=True, methods='POST')
@frappe.whitelist(allow_guest=True)
def login(user, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(user=user, pwd=pwd)
        login_manager.post_login()
        
        mp_roles = get_mp_roles(frappe.session.user)

        user_details = generate_api_keys(frappe.session.user)

        token = get_jwt(user_details, mp_roles)
    
        success_auth_reponse({'token': token})
    
    except Exception as e:
        print(e)
        login_manager.logout()
        frappe.clear_messages()
        failed_auth_response()


@frappe.whitelist(allow_guest=True)
def logout():
    remove_api_key(frappe.session.user)
    LoginManager().logout()
    success_auth_reponse()
