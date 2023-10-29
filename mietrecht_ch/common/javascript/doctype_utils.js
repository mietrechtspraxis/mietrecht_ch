function setMonthToSecondToLast(frm) {
    if (!frm.doc.monat) {
        var today = new Date();
        var begginingOfLastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
        var monatString = `${begginingOfLastMonth.getFullYear()}-${(begginingOfLastMonth.getMonth() + 1).toString().padStart(2, '0')}-01`;
        frm.set_value('monat', monatString );
    }
}

function checkUrl(url) {
    var pattern = /^(\/|https?:\/\/)/;
    pattern.test(url);
    if (!pattern.test(fieldRedirect)) {
        frappe.throw(`The url ${url} used is not a conform url. Please use a valid url starting with '/' , 'http://' or 'https://'.'`);
    }
}