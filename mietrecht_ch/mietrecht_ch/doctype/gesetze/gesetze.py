# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

# OR <article-number> 	<abs-number> <lit-nr>
# OR 253a 
# OR 253a 				2
# OR 256							 a.

class Gesetze(Document):
	def autoname(self):
		self.name = """{} {}""".format(self.law_type, self.article_number.strip())
		if self.section_number != None:
			self.name = """{} {}""".format(self.name, self.section_number)
