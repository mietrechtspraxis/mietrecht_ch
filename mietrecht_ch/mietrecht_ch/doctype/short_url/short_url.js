// Copyright (c) 2023, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Short URL', {
	validate(frm) {
		const fieldUri = frm.doc.uri
		const fieldRedirect = frm.doc.redirect
		checkUrl(fieldRedirect)
		cleanUri(fieldUri)

		function cleanUri(uri) {
			const regex = /^[A-Za-z0-9]+(?:[-/][A-Za-z0-9]+)*$/;

			if (fieldUri.startsWith('/') || fieldUri.endsWith('/') ) {
				frappe.throw("Uri cannot start or end with a /.")
			}
	
			if (!regex.test(fieldUri)) {
				const newUriValue = fieldUri.replace(/[^0-9A-Za-z-\/]/g, "");
				frm.set_value('uri', newUriValue)
			}
		}
		function checkUrl(url) {
			var pattern = /^(\/|https?:\/\/)/;
			pattern.test(url);
			if (!pattern.test(fieldRedirect)) {
				frappe.throw(`The url ${url} used is not a conform url. Please use a valid url starting with '/' , 'http://' or 'https://'.'`);
			}
		}
	}
});

frappe.ui.form.on('Short URL', {
	test_redirect: function(frm) {
		if (window.location.hostname == "mietrecht.localhost") {
			var webserver = 'mietrecht.localhost:4200';
		} else if (window.location.hostname == 'erpnext.staging.mietrecht.ch' ) {
			var webserver = 'staging.mietrecht.ch';
		} else {
			var webserver = 'mietrecht.ch' ;
		}
		var openlink = window.open('https://'+ webserver +'/'+frm.doc.uri);
	}
});