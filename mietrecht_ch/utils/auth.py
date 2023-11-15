import frappe
from frappe.auth import LoginManager

MP_WEB_USER_ROLE = "mp_web_user_abo"
MP_WEB_ADMIN_ROLE = "mp_web_admin"

@frappe.whitelist(allow_guest=True)
def get_token(user, pwd, expires_in=3600, expire_on=None):
    
  if not frappe.db.exists("User", user):
    raise frappe.ValidationError(_("Invalide User")) 

  login = LoginManager()
  return login
