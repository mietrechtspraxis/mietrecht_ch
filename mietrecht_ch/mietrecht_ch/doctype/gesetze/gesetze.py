# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class Gesetze(Document):
	def autoname(self):
		self.name = self.__set_name__()
		# if name == self.name: return 
		
		
	def __get_name__(self):
		name = """Art. {}""".format(self.article_number.strip())
		if self.section_number != None:
			name += """ Abs. {} """.format(self.section_number.strip())
		if self.lit_number != None:
			name += """ lit. {} """.format(self.lit_number.strip())
		name += """ {}""".format(self.law_type)
		return name
