# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils.data import add_days, today, now
from frappe.utils import cint
from mietrecht_ch.mietrecht_ch.doctype.antwort_auf_das_formular.api import __add_role_mp__, __create_base_user__
from frappe.exceptions import DoesNotExistError
from mietrechtspraxis.mietrechtspraxis.utils.qrr_reference import get_qrr_reference

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
        if not self.first_name and not self.company:
            frappe.throw("Es muss entweder ein Vorname oder eine Firma hinterlegt sein.")
        if not self.street:
            frappe.throw("Es muss eine Strasse angegeben werden.")
        if cint(self.different_delivery_address) == 1:
            if not self.delivery_first_name and not self.delivery_company:
                frappe.throw("Es muss entweder ein Vorname oder eine Firma hinterlegt sein.")
            if not self.delivery_zip_and_city:
                frappe.throw("Es müssen PLZ und Ort angegeben werden.")
            if not self.delivery_street:
                frappe.throw("Es muss eine Strasse angegeben werden.")
        if not self.customer:
            customer = create_customer(self)
            self.customer = customer
        
        if not self.contact:
            contact = create_contact(self)
            self.contact = contact
        
        if cint(self.different_delivery_address) == 1 and not self.second_contact:
            contact = create_contact(self, True)
            self.second_contact = contact
        
        if self.type == 'abo':
            mp_abo = create_mp_abo(self)
        elif self.type == 'shop':
            mp_abo = create_sales_order(self, cint(self.different_delivery_address))
        else:
            frappe.throw("Im Moment können nur Abo- und Shop-Bestellungen verarbeitet werden.")
    
    def check_grand_total(self):
        if self.sales_order:
            data = json.loads(self.data)
            grand_total = data.get('total')
            so = frappe.get_doc("Sales Order", self.sales_order)
            if so.grand_total != grand_total:
                frappe.throw("Achtung, der Totalbetrag stimmt nicht überein!")


def get_abo_mapper():
    abo_mapper = {
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "jahres_abo")): 'Jahres-Abo',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "jahres_legi_abo")): 'Jahres-Legi-Abo',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "gratis_abo")): 'Gratis-Abo',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "probe_abo")): 'Probe-Abo',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "jahres_abo_digital")): 'Jahres-Abo Digital',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "jahres_legi_abo_digital")): 'Jahres-Legi-Abo Digital',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "gratis_abo_digital")): 'Gratis-Abo Digital',
        '{0}'.format(frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "probe_abo_digital")): 'Probe-Abo Digital'
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
    digital = False
    type = formular.abo_type
    if "Digital" in formular.abo_type:
        type = formular.abo_type.replace(" Digital", "")
        digital = 1
    
    mp_abo = frappe.get_doc({
        "doctype": "mp Abo",
        "invoice_recipient": formular.customer,
        "recipient_contact": formular.contact,
        "recipient_address": frappe.db.get_value("Contact", formular.contact, "address"),
        "recipient": [
            {
                "abo_type": type,
                "digital": cint(digital),
                "magazines_qty_mr": 0 if digital else 1,
                "magazines_recipient": formular.customer,
                "recipient_contact": formular.contact,
                "recipient_address": frappe.db.get_value("Contact", formular.contact, "address")
            }
        ]
    })
    mp_abo.insert()
    
    formular.mp_abo = mp_abo.name
    formular.conversion_date = today()
    formular.status = 'Closed'
    formular.save()

    return

def create_sales_order(formular, different_delivery_address=False):
    data = json.loads(formular.data)
    products = data.get('products')

    items = []
    for key, value in products.items():
        items.append({
            "item_code": key,
            "qty": value,
            "rate": get_price(key),
            "price_list_rate": get_price(key)
        })
    
    # Sales Order
    try:
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": formular.customer,
            "customer_address": frappe.db.get_value("Contact", formular.contact, "address"),
            "shipping_address_name": frappe.db.get_value("Contact", formular.second_contact, "address") if different_delivery_address == 1 else None,
            "contact_person": formular.contact,
            "items": items,
            "delivery_date": today(),
            "taxes_and_charges": "Gemischte MWST - mp"
        })
        so.insert()
        so.submit()
        formular.sales_order = so.name
        attach_pdf(formular, so)
    except Exception as so_err:
        frappe.log_error("{0}".format(so_err), 'AADF: Sales Order')
        pass

    # Delivery Note
    try:
        from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
        dn = make_delivery_note(so.name)
        if different_delivery_address == 1:
            dn.contact_person = formular.second_contact
        dn.save()
        dn.submit()
        formular.delivery_note = dn.name
        attach_pdf(formular, dn)
    except Exception as dn_err:
        frappe.log_error("{0}".format(dn_err), 'AADF: Delivery Note')
        pass

    # Sales Invoice
    try:
        from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
        sinv = make_sales_invoice(so.name)
        sinv.save()
        sinv.esr_reference = get_qrr_reference(sales_invoice=sinv.name, customer=formular.customer)
        sinv.save(ignore_permissions=True)
        sinv.submit()
        formular.sales_invoice = sinv.name
        attach_pdf(formular, sinv)
    except Exception as sinv_err:
        frappe.log_error("{0}".format(err), 'AADF: Sales Invoice')
        pass

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
    frappe.db.commit()

    return customer.name

def create_contact(formular, second=False):
    # contact
    if not second:
        salutation = formular.gender
        first_name = formular.first_name or formular.company
    else:
        salutation = formular.delivery_gender
        first_name = formular.delivery_first_name or formular.delivery_company
    salutation = None if salutation == 'keines von beiden' else salutation

    contact = frappe.get_doc({
        "doctype": "Contact",
        'first_name': first_name,
        'last_name': formular.last_name if not second else formular.delivery_last_name,
        'salutation': salutation,
        'links': [
            {
                'link_doctype': 'Customer',
                'link_name': formular.customer
            }
        ]
    })
    contact.insert()
    frappe.db.commit()

    # address
    contact.address = create_address(formular, second)

    # mp web user
    if formular.email:
        mp_web_user = create_mp_web_user(formular)
        contact.mp_web_user = mp_web_user
        row = contact.append('email_ids', {})
        row.email_id = formular.email
        row.is_primary = 1
    
    contact.save(ignore_permissions=True)
    frappe.db.commit()

    return contact.name

def create_address(formular, second=False):
    postfach = 0
    if not second:
        postfach = 1 if formular.po_box else 0
    else:
        postfach = 1 if formular.delivery_po_box else 0
    
    address = frappe.get_doc({
        "doctype": "Address",
        'address_title': formular.customer if not second else "Lieferung: {0}".format(formular.customer),
        'zusatz': formular.additional_info if not second else formular.delivery_additional_info,
        'strasse': formular.street if not second else formular.delivery_street,
        'address_line1': formular.street if not second else formular.delivery_street,
        'postfach': postfach,
        'plz': formular.zip_and_city.split(" ")[0] if not second else formular.delivery_zip_and_city.split(" ")[0],
        'pincode': formular.zip_and_city.split(" ")[0] if not second else formular.delivery_zip_and_city.split(" ")[0],
        'city': formular.zip_and_city.replace(formular.zip_and_city.split(" ")[0] + " ", "") if not second else formular.delivery_zip_and_city.replace(formular.delivery_zip_and_city.split(" ")[0] + " ", ""),
        'links': [
            {
                'link_doctype': 'Customer',
                'link_name': formular.customer
            }
        ]
    })
    address.insert()
    frappe.db.commit()

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

def attach_pdf(formular, doc_record):
    # erstellung Rechnungs PDF
    from PyPDF2 import PdfFileWriter
    from frappe.utils.pdf import get_file_data_from_writer
    output = PdfFileWriter()

    printformat = "Standard"
    if doc_record.doctype == 'Sales Invoice':
        printformat = "Verlagsprodukte"
    elif doc_record.doctype == 'Sales Order':
        printformat = "Verlagsprodukte SO"
    elif doc_record.doctype == 'Delivery Note':
        printformat = "Verlagsprodukte DN"
    
    output = frappe.get_print(doc_record.doctype, doc_record.name, printformat, as_pdf = True, output = output, ignore_zugferd=True)
    
    file_name = "{docname}_{datetime}".format(docname=doc_record.name, datetime=now().replace(" ", "_"))
    file_name = file_name.split(".")[0]
    file_name = file_name.replace(":", "-")
    file_name = file_name + ".pdf"
    
    filedata = get_file_data_from_writer(output)
    
    _file = frappe.get_doc({
        "doctype": "File",
        "file_name": file_name,
        "folder": "Home/Attachments",
        "is_private": 1,
        "content": filedata,
        "attached_to_doctype": 'Antwort auf das Formular',
        "attached_to_name": formular.name
    })
    
    _file.save(ignore_permissions=True)

def get_price(item_code):
    prices = frappe.db.sql("""SELECT
                                    `price_list_rate`
                                FROM `tabItem Price`
                                WHERE `selling` = 1
                                AND `item_code` = '{item_code}'
                                AND (
                                    `valid_from` IS NULL
                                    OR
                                    `valid_from` <= CURDATE()
                                )
                                AND (
                                    `valid_upto` IS NULL
                                    OR
                                    `valid_upto` >= CURDATE()
                                )
                           """.format(item_code=item_code), as_dict=True)
    if prices:
        return prices[0].price_list_rate
    else:
        return None
