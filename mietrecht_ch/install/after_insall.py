# my_app/install/before_install.py

from __future__ import unicode_literals

import frappe

def execute():
    # Create or update roles
    create_or_update_mp_roles()

def create_or_update_mp_roles():
    # Check if the role already exists, if not, create it
    for role_name in ["mp_web_user_abo", "mp_web_admin"]:
        if not frappe.get_all("Role", filters={"role_name": role_name}):
            print("Roles do not exsits")
            # role = frappe.new_doc("Role")
            # role.role_name = role_name
            # role.save(ignore_permissions=True)
        else :
            print("Roles exsit")
