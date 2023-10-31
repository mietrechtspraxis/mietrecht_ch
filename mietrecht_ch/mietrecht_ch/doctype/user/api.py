import frappe
from frappe import _
from frappe.auth import LoginManager
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.models.jwt import JWTGenerator

login = LoginManager()

@frappe.whitelist(allow_guest=True)
def get_token(user, expires_in=3600, expire_on=None):
    login = LoginManager()
    token = JWTGenerator('secret')
    
    if not frappe.db.exists("User", user):
        raise frappe.ValidationError(_("Invalide User")) 
    
    payload = {'some': 'payload'}
    
    generated_jwt = token.generate_token(payload)
    decoded_jwt = token.decode_token(generated_jwt)
    return generated_jwt, decoded_jwt

    if not login.check_password(user, 'mietrecht*'):
        login.fail('Incorrect password', user=user)
        
    # return the apu key created, but by hand so need to find a way to generate it by code.
    #frappe.db.get_value('User', 'Guest', 'api_key')
  
    # integrate jwt to generate a token
    # maybe find a way to generate a has using hashlib
    return

@frappe.whitelist(allow_guest=True)
def reset_password(user, email):
    
    if (len(user) == 0 and user is None) and (len(email) == 0 and email is None):
        raise BadRequestException('User and password cannot be empty.')
    
    check_email = frappe.db.get_value('User', user, "email")

    if bool(email != check_email):
        raise BadRequestException("Email don't match.")
        
    # envoie d'email avec link to reset a password.
    
    if not frappe.db.exists("User", user):
        raise frappe.ValidationError(_("Invalide User")) 
