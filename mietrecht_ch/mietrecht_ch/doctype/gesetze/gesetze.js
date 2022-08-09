// Copyright (c) 2022, mietrecht.ch and contributors
// For license information, please see license.txt
const DOCTYPE = 'Gesetze';

frappe.ui.form.on(DOCTYPE, {
	after_save: function() {
		frappe.set_route("List", DOCTYPE);
	}
});
