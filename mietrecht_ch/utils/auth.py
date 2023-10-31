import frappe
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def get_token(user, pwd, expires_in=3600, expire_on=None):
    
  if not frappe.db.exists("User", user):
    raise frappe.ValidationError(_("Invalide User")) 

  login = LoginManager()
  return login
