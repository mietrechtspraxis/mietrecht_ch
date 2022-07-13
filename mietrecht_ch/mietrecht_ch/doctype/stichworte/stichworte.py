# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Stichworte(Document):

	def validate(self):
		self.build_breadcrum()
		self.update_auto_name()

	def update_auto_name(self):
		self.name = '{} ({})'.format(self.item_name, self.name)

	def build_breadcrum(self):
		node = self
		breadcrum = self.item_name
		while (node.parent_stichworte != None):
			parent = frappe.get_doc('Stichworte', node.parent_stichworte)
			breadcrum = parent.item_name + ' > ' + breadcrum
			node = parent
		self.breadcrum = breadcrum
