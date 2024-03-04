// Copyright (c) 2023, mietrecht.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Antwort auf das Formular', {
    formular_verarbeiten: function(frm) {
        if (cur_frm.is_dirty()) {
            cur_frm.save().then(function(){
                verarbeiten(frm);
            })
        } else {
            verarbeiten(frm);
        }
    },
    refresh: function(frm) {
        check_grand_total(frm);
    }
});

function verarbeiten(frm) {
    if((!cur_frm.doc.kunde_nicht_vorhanden)&&(!cur_frm.doc.customer)) {
        frappe.msgprint("Bitte prüfen ob der entsprechende Kunde existiert.");
    } else if((!cur_frm.doc.kontakt_nicht_vorhanden)&&(!cur_frm.doc.contact)) {
        frappe.msgprint("Bitte prüfen ob der entsprechende Kontakt existiert.");
    } else if((!cur_frm.doc.abweichender_kontakt_nicht_vorhanden)&&(!cur_frm.doc.second_contact)&&(cur_frm.doc.different_delivery_address)) {
        frappe.msgprint("Bitte prüfen ob der entsprechende, abweichende, Kontakt existiert.");
    } else if(cur_frm.doc.status != 'Open') {
        frappe.msgprint("Das Formular wurde bereits verarbeitet.");
    } else {
        frappe.call({
            method: 'formular_verarbeiten',
            doc: frm.doc,
            freeze: true,
            freeze_message: "Bitte warten...",
            callback: function(response) {
                cur_frm.reload_doc();
                frappe.show_alert("Das Formular wurde verarbeitet");
            }
        });
    }
}

function check_grand_total(frm) {
    frappe.call({
        method: 'check_grand_total',
        doc: cur_frm.doc,
        freeze: true,
        freeze_message: "Prüfe Total...",
        callback: function(r) {
            frappe.show_alert("Das Total wurde geprüft");
        }
    });
}
