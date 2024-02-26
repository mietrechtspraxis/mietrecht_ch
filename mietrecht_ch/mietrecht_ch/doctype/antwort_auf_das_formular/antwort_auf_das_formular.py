# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils.data import add_days, today
from frappe.utils import cint
from mietrecht_ch.mietrecht_ch.doctype.antwort_auf_das_formular.api import __add_role_mp__, __create_base_user__
from frappe.exceptions import DoesNotExistError

class AntwortaufdasFormular(Document):
    def validate(self):
        self.set_missing_values()
    
    def set_missing_values(self):
        self.set_abo_type()
        self.set_login_expiration_date()
    
    def set_abo_type(self):
        if self.abo_type == 'Undefiniert':
            if self.type == 'abo':
                data = json.loads(self.data)
                if data:
                    abo_item = data.get('abo')
                    abo_mapper = get_abo_mapper()
                    try:
                        abo = abo_mapper[abo_item]
                        self.abo_type = abo
                    except:
                        pass
    
    def set_login_expiration_date(self):
        if self.type == 'abo' and self.abo_type:
            login_expiration = get_login_expiration(self.abo_type)
            self.login_expiration_date = add_days(self.creation or today(), int(login_expiration))
    
    def formular_verarbeiten(self):
        if not self.customer:
            customer = create_customer(self)
            self.customer = customer
        
        if not self.contact:
            contact = create_contact(self)
            self.contact = contact
        
        if self.type == 'abo':
            mp_abo = create_mp_abo(self)
        elif self.type == 'shop':
            mp_abo = create_sales_order(self)
        else:
            frappe.throw("Im Moment können nur Abo- und Shop-Bestellungen verarbeitet werden.")


def get_abo_mapper():
    abo_mapper = {
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "jahres_abo")): 'Jahres-Abo',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "gratis_abo")): 'Gratis-Abo',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "probe_abo")): 'Probe-Abo'
    }

    return abo_mapper

def get_login_expiration(abo_type):
    if abo_type == 'Jahres-Abo':
        return frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "login_ablauf_reg_abo")
    elif abo_type == 'Gratis-Abo':
        return 365
    elif abo_type == 'Probe-Abo':
        return frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "login_ablauf_probe_abo")
    else:
        return frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "login_ablauf")

def create_mp_abo(formular):
    mp_abo = frappe.get_doc({
        "doctype": "mp Abo",
        "type": formular.abo_type,
        "invoice_recipient": formular.customer,
        "recipient_contact": formular.contact,
        "recipient_address": frappe.db.get_value("Contact", formular.contact, "address")
    })
    mp_abo.insert()
    
    formular.mp_abo = mp_abo.name
    formular.conversion_date = today()
    formular.status = 'Closed'
    formular.save()

    return

def create_sales_order(formular):
    data = json.loads(formular.data)
    products = data.get('products')

    items = []
    for key, value in products.items():
        items.append({
            "item_code": key,
            "qty": value
        })
    
    so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": formular.customer,
        "customer_address": frappe.db.get_value("Contact", formular.contact, "address"),
        "contact_person": formular.contact,
        "items": items,
        "delivery_date": today()
    })
    so.insert()

    formular.sales_order = so.name
    formular.conversion_date = today()
    formular.status = 'Closed'
    formular.save()

    return

def create_customer(formular):
    if not formular.company:
        customer_name = " ".join([formular.first_name, formular.last_name]) if formular.first_name else formular.last_name or 'Keine Angaben'
    else:
        customer_name = formular.company
    
    customer = frappe.get_doc({
        "doctype": "Customer",
        'customer_name': customer_name,
        'customer_type': 'Individual' if not formular.company else 'Company'
    })
    customer.insert()

    return customer.name

def create_contact(formular):
    # contact
    contact = frappe.get_doc({
        "doctype": "Contact",
        'first_name': formular.first_name,
        'last_name': formular.last_name,
        'salutation': formular.gender,
        'links': [
            {
                'link_doctype': 'Customer',
                'link_name': formular.customer
            }
        ]
    })
    contact.insert()

    # address
    contact.address = create_address(formular)

    # mp web user
    if formular.email:
        mp_web_user = create_mp_web_user(formular)
        contact.mp_web_user = mp_web_user
        row = contact.append('email_ids', {})
        row.email_id = formular.email
        row.is_primary = 1
    
    contact.save(ignore_permissions=True)

    return contact.name

def create_address(formular):
    address = frappe.get_doc({
        "doctype": "Address",
        'address_title': formular.customer,
        'zusatz': formular.additional_info,
        'strasse': formular.street,
        'address_line1': formular.street,
        'postfach': 1 if formular.po_box else 0,
        'plz': formular.zip_and_city.split(" ")[0],
        'city': formular.zip_and_city.replace(formular.zip_and_city.split(" ")[0] + " ", ""),
        'links': [
            {
                'link_doctype': 'Customer',
                'link_name': formular.customer
            }
        ]
    })
    address.insert()

    return address.name

def create_mp_web_user(formular):
    try:
        user = frappe.get_doc('User', formular.email)
        __add_role_mp__(user)
    except DoesNotExistError:
        request_data = {
            'email': formular.email,
            'billing_address': {
                'first_name': formular.first_name,
                'last_name': formular.last_name
            }
        }
        user = __create_base_user__(request_data)
        __add_role_mp__(user)
    except Exception as err:
        frappe.throw("{0}".format(err))
    finally:
        return user.name

