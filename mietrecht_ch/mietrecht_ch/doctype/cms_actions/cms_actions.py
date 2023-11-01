# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import re

class CMSActions(Document):
	def validate(self):
		self.check_if_internal()
		self.allow_one_field()
  
	def check_if_internal(self):
     
		check_url = self.not_empty_string_allowed()

		if bool(check_url) == True:
			self.is_internal = 0
		else:
			self.is_internal = 1
   
	def allow_one_field(self):
		url = self.url
		file = self.file
		if len(url) != 0 and file is not None:
			frappe.throw("Please add either a url OR a file not both.")
		
	def not_empty_string_allowed(self):
		pattern = r'https?://'

		if len(self.url) == 0:
			frappe.throw("url cannot be empty.")	

		return re.search(pattern, self.url)