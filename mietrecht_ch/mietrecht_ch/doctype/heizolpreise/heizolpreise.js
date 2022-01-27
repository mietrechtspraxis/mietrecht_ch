// Copyright (c) 2022, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Heizolpreise', {
	onload: function(frm) {
		if (!frm.doc.monat) {
			var today = new Date();
			frm.set_value('monat', new Date(today.getFullYear(), today.getMonth(), 1));
		}
	}
});
