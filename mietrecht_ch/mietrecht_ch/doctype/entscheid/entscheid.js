// Copyright (c) 2022, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entscheid', {
	open_id_old: function(frm) {
		var openlink = window.open('https://www.mietrecht.ch/db/mr_entsch_show.php?id='+frm.doc.id_old, '_blank', 'popup=yes');
	},
	open_web: function(frm) {
		var baseUrl
		if (window.location.hostname == "mietrecht.localhost") {
			baseUrl = 'http://localhost:4200/entscheide/';
		} else if (window.location.hostname == 'mp.libracore.ch' ) {
			baseUrl = 'https://staging2.mietrecht.ch/entscheide/';
		} else if (window.location.hostname == 'mp-test.libracore.ch') {
			baseUrl = 'https://staging2.mietrecht.ch/entscheide/';
		} else {
			baseUrl = 'https://mietrecht.ch/entscheide/';
		}
		var openlink = window.open(baseUrl + frm.doc.name, '_blank', 'popup=yes');
	 }
});