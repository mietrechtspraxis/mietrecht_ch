// Copyright (c) 2023, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Short URL', {
	validate(frm) {
		const fieldUri = frm.doc.uri
		const fieldRedirect = frm.doc.redirect
		checkUrl(fieldRedirect)
		cleanUri(fieldUri)

		function cleanUri(uri) {
			const regex = /^[A-Za-z0-9-]+$/;
	
			if (!regex.test(fieldUri)) {
				const newUriValue = fieldUri.replace(/[^0-9A-Za-z-]/g, "");
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
