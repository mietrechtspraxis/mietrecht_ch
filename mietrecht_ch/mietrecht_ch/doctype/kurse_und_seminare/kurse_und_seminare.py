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
	format_string = translate_string(self.title)
	without_accents = ''.join(c for c in unicodedata.normalize('NFD', format_string) if not unicodedata.combining(c))

	# Remove special characters (keep only alphanumeric characters and spaces)
	without_special_chars = re.sub(r'[^a-zA-Z0-9\s]', '', without_accents)
 
	return without_special_chars

def translate_string(text):
   # Define a dictionary to map special characters to their replacements
	char_replacements = {
		'ä': 'ae',
		'ö': 'oe',
		'ü': 'ue',
		'Ä': 'ae',
		'Ö': 'oe',
		'Ü': 'ue',
	}

	# Create a regex pattern that matches any of the special characters
	pattern = re.compile('|'.join(map(re.escape, char_replacements.keys())))

	# Use the sub() method to replace the characters based on the pattern
	return pattern.sub(lambda match: char_replacements[match.group(0)], text)

		
