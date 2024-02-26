// Copyright (c) 2023, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Antwort auf das Formular', {
    formular_verarbeiten: function(frm) {
        if (cur_frm.is_dirty()) {
            frappe.msgprint("Bitte speichern Sie das Formular zuerst")
        } else {
            if((!cur_frm.doc.kunde_nicht_vorhanden)&&(!cur_frm.doc.customer || !cur_frm.doc.contact)) {
                frappe.msgprint("Bitte prüfen ob der entsprechende Kunde existiert.");
            } else if(cur_frm.doc.status != 'Open') {
                frappe.msgprint("Das Formular wurde bereits verarbeitet.");
            } else {
                frappe.call({
                    method: 'formular_verarbeiten',
                    doc: frm.doc,
                    callback: function(response) {
                        cur_frm.reload_doc();
                       frappe.show_alert("Das Formular wurde verarbeitet");
                    }
                });
            }
        }
    }
});
