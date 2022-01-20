import frappe


@frappe.whitelist(allow_guest=True)
def get_all_heizolpreise(reference, year, month):
    return frappe.db.sql("""SELECT `monat`, `{reference}` 
                            FROM `tabHeizolpreise` 
                            WHERE `monat` LIKE '{year}-{month}-%';""".format(reference=reference, year=year, month=str.zfill(month, 2)), as_dict=True)
