import frappe


@frappe.whitelist(allow_guest=True)
def get_single_oil_price(quantity, year, month):
    return frappe.db.sql("""SELECT `monat` as `month`, `{quantity}` as `price`, '{quantity}' as `quantity`
                            FROM `tabHeizolpreise` 
                            WHERE `monat` LIKE '{year}-{month}-01';""".format(quantity=quantity, year=year, month=str.zfill(month, 2)), as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_multiple_oil_price(quantity, fromYear, fromMonth, toYear, toMonth):
    return frappe.db.sql("""SELECT `monat` as `month`, `{quantity}` as `price`, '{quantity}' as `quantity`
                            FROM `tabHeizolpreise` 
                            WHERE `monat` BETWEEN '{fromYear}-{fromMonth}-01' AND '{toYear}-{toMonth}-01' ;"""
                            .format(quantity=quantity, fromYear=fromYear, toYear=toYear, fromMonth=str.zfill(fromMonth, 2), toMonth=str.zfill(toMonth, 2)), as_dict=True)
