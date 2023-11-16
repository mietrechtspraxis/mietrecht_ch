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
		url = self.url
		file = self.file
		if (len(url) == 0) and file is None :
			frappe.throw("Please add either a url OR a file not both.")
		
	def not_empty_string_allowed(self):
		pattern = r'(https?://|/)'
  
		if self.url == "":
			return

		match = re.search(pattern, str(self.url))
  
		if not match:
			frappe.throw("The url must start with https:// - http:// or /")


