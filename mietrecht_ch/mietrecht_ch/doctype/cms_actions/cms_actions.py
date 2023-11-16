# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import re

class CMSActions(Document):
	def validate(self):
		self.allow_one_field()
		self.check_if_internal()
  
	def check_if_internal(self):
     
		check_url = self.not_empty_string_allowed()

		if bool(check_url) == True:
			self.is_internal = 0
		else:
			self.is_internal = 1
   
	def allow_one_field(self):  
		filled_fields = [field for field in [self.url, self.file_url, self.file_attachment] if field ]

		if len(filled_fields) > 1:
			frappe.throw("Please only fill either 'Url' or 'File Url' or 'File Attachement'.")

        
	def not_empty_string_allowed(self):
		pattern = r'(https?://|/)'
  
		if self.url == "":
			return

		match = re.search(pattern, str(self.url))
  
		if not match:
			frappe.throw("The url must start with https:// - http:// or /")


