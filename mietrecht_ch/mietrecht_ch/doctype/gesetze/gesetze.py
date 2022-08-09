# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Gesetze(Document):
	# only called on new element creation
	def autoname(self):
		self.name = self.__get_name__()

	# only called when updating the element
	def on_update(self):
		# check if information used in the name has been changed
		if (
			self.has_value_changed('article_number') or
			self.has_value_changed('paragraph_number') or
			self.has_value_changed('letter_number') or
			self.has_value_changed('law_type')
		):
			frappe.rename_doc(self.doctype, self.name, self.__get_name__(), force=False, merge=False, ignore_permissions=False, ignore_if_exists=False)
			frappe.db.commit()
		
	def __get_name__(self):
		name = """Art. {}""".format(self.article_number.strip())
		if self.paragraph_number != None:
			name += """ Abs. {}""".format(self.paragraph_number.strip())
		if self.letter_number != None:
			name += """ lit. {}""".format(self.letter_number.strip())
		name += """ {}""".format(self.law_type)
		return name
