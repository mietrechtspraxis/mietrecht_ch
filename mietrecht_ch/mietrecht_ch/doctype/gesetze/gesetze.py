# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Gesetze(Document):
	def autoname(self):
		self.name = self.__get_name__()

	def on_update(self):
		if (
			self.has_value_changed('article_number') or
			self.has_value_changed('paragraph_number') or
			self.has_value_changed('lit_number') or
			self.has_value_changed('law_type')
		):
			frappe.rename_doc(self.doctype, self.name, self.__get_name__(), force=False, merge=False, ignore_permissions=False, ignore_if_exists=False)
			frappe.db.commit()
		
	def __get_name__(self):
		name = """Art. {}""".format(self.article_number.strip())
		if self.paragraph_number != None:
			name += """ Abs. {} """.format(self.paragraph_number.strip())
		if self.lit_number != None:
			name += """ lit. {} """.format(self.lit_number.strip())
		name += """ {}""".format(self.law_type)
		return name
