import frappe
from frappe import _
from frappe.auth import LoginManager
import jwt
@frappe.whitelist(allow_guest=True)
def get_token(user, expires_in=3600, expire_on=None):
    
  if not frappe.db.exists("User", user):
    raise frappe.ValidationError(_("Invalide User")) 

  login = LoginManager()
  login.check_password(user, 'mietrecht')
  
  token = jwt.encode()
  return 
