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
		url = self.url
		file_url = self.file_url
  
		check_url = ''
		if url is not None and len(url) != 0:
			check_url = not_empty_string_allowed(url)
		if file_url is not None and len(file_url) != 0:
			check_url = not_empty_string_allowed(file_url)
  
		if check_start(check_url) == True:
			self.is_internal = 0
		else:
			self.is_internal = 1
   
	def allow_one_field(self):  
		filled_fields = [field for field in [self.url, self.file_url, self.file_attachment] if field ]

		if len(filled_fields) > 1:
			frappe.throw("Please only fill either 'Url' or 'File Url' or 'File Attachement'.")

        
def not_empty_string_allowed(field):
	pattern = r'(https?://|/)'

	if field is not None and len(field) != 0:

		match = re.search(pattern, str(field))
  
		if not match:
			frappe.throw("The 'Url' or 'File Url' field must start with https:// - http:// or /")
		return field

def check_start(string):
    if string.startswith("http") or string.startswith("https"):
        return True
    else:
        return False


