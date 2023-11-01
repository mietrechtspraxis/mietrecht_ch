# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class CMSActions(Document):
	def validate(self):
		self.check_if_internal()
  
	def check_if_internal(self):
		check_url = self.url.startswith("http://") or self.url.startswith("https://")
		print(check_url)
		if check_url == True:
			self.is_internal == 0
		else:
			self.is_internal == 1
