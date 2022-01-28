// Copyright (c) 2022, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Heizolpreise', {
	onload: function(frm) {
		if (!frm.doc.monat) {
			var today = new Date();
			var begginingOfLastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
			var monatString = `${begginingOfLastMonth.getFullYear()}-${(begginingOfLastMonth.getMonth() + 1).toString().padStart(2, '0')}-01`;
			frm.set_value('monat', monatString );
		}
	}
});
