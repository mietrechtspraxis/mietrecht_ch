# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime_str, formatdate

class Heizolpreise(Document):
	def autoname(self):
		_date = formatdate(get_datetime_str(self.monat), "yyyy-MM-dd")
		self.name = "heizolpreise-{}".format(_date)
