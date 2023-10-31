import frappe
from frappe import _
from frappe.auth import LoginManager
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.models.jwt import JWTGenerator

login = LoginManager()

@frappe.whitelist(allow_guest=True)
def auth(user, expires_in=3600, expire_on=None):
    login = LoginManager()
    token = JWTGenerator('secret')
    
    # Email used to check not name
    if not frappe.db.exists("User", user):
        raise frappe.ValidationError(_("Invalide User"))
    
    # check password first
    if not login.check_password(user, 'mietrecht*'):
        login.fail('Incorrect password', user=user)
    # Get use informations from doctype
    get_info_user = frappe.db.get_value('User', user, ['name', 'first_name','last_name', 'role_profile_name', 'api_key'], as_dict=1)
    user_role = get_info_user.role_profile_name
  
    # Defining the JWT
    payload = {'user': user, 'role': user_role}
    generated_jwt = token.generate_token(payload)
    decoded_jwt = token.decode_token(generated_jwt)
    return decoded_jwt


@frappe.whitelist(allow_guest=True)
def reset_password(user, email):
    
    if (len(user) == 0 and user is None) and (len(email) == 0 and email is None):
        raise BadRequestException('User and password cannot be empty.')
    
    check_email = frappe.db.get_value('User', user, "email")

    if bool(email != check_email):
        raise BadRequestException("Email don't match.")
        
    # envoie d'email avec link to reset a password.
    recipients = [
    'david.planchon@liip.ch',
    ]      
    
    reset_password_link = 'http://reset-password'
    message = 'Hello, here is you link to reset your password because your email matched our database.'

    frappe.sendmail(
        recipients=recipients,
        subject=frappe._('Password reseting'),
        args=dict(
            reset_password_link=reset_password_link,
            message=message,
        ),
        header=_('Password resetting')
    )
    
