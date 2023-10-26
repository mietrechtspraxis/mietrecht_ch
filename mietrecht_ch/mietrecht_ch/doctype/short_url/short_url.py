# -*- coding: utf-8 -*-
# Copyright (c) 2023, mietrecht.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
from frappe.model.document import Document
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException


class ShortURL(Document):
	def validate(self):
		self.check_if_valid_url()
  
	def check_if_valid_url(self):
		pattern = re.compile(r'^(?:/|https?://)')
		
		if not pattern.match(self.redirect):
			frappe.throw(f"The url {self.redirect} used is not a conform url. Please use a valid url starting with '/' , 'http://' or 'https://'.")