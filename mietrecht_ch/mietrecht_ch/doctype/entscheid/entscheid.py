# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Entscheid(Document):
	def validate(self):
		if(self.type == "Flash"):
			self.validate_flash()
		if (self.type == "Aufsatz"):
			self.validate_aufsatz()
	
	def validate_flash(self):
		currentType = "Flash"
		self.required_field(self.mp_flash, "MP Flash", currentType )
		self.required_field(self.mp_flash_summary, "MP Flash Summary", currentType )

	def validate_aufsatz(self):
		currentType = "Aufsatz"
		self.required_field(self.author_de, "Author (DE)", currentType )
		self.required_field(self.author_info_de, "Author Info (DE)", currentType )

	def required_field(self, value, fieldName, type):
		if (value == None):
			frappe.throw("Das Feld {} ist bei der Erstellung eines {} erforderlich".format(fieldName, type))
