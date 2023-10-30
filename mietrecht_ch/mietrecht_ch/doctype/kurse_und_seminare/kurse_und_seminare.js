// Copyright (c) 2023, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kurse und Seminare', {
	validate: function(frm) {
		checkUrl(frm.doc.iframe_uri)

		function checkUrl(url) {
			var pattern = /^(\/|https?:\/\/)/;
			pattern.test(url);
			if (!pattern.test(url)) {
				frappe.throw(`The url ${url} used is not a conform url. Please use a valid url starting with '/' , 'http://' or 'https://'.'`);
			}
		}
	}
});
