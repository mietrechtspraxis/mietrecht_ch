# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import unicodedata
import re
from frappe.model.document import Document

class KurseundSeminare(Document):
	def autoname(self):
		self.name = remove_special_characters_and_accents(self)

     
def remove_special_characters_and_accents(self):
	without_accents = ''.join(c for c in unicodedata.normalize('NFD', self.title) if not unicodedata.combining(c))

	# Remove special characters (keep only alphanumeric characters and spaces)
	without_special_chars = re.sub(r'[^a-zA-Z0-9\s]', '', without_accents)

	return without_special_chars

		
