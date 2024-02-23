# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils.data import add_days, today

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
        return 36500
    elif abo_type == 'Probe-Abo':
        return frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "login_ablauf_probe_abo")
    else:
        return frappe.db.get_value("mp Abo Settings", "mp Abo Settings", "login_ablauf")
