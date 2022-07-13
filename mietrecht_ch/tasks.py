import frappe

LIMIT_STOCK = 3


def ebook_cron():

    ebook_quantity = __ebook_quantity__()

    if ebook_quantity <= LIMIT_STOCK:
        __ebook_sendmail__(ebook_quantity)


def __ebook_quantity__():
    ebook_doctype = frappe.db.get_list('Voucher',
                                       filters={
                                           'associated_pak': ''
                                       })
    number_ebook_available = len(ebook_doctype)
    return number_ebook_available


def __ebook_sendmail__(ebook_quantity):

    email_list_formatted = __get_email_list__()
    print(email_list_formatted[0])
    if email_list_formatted is not None and '':
        frappe.sendmail(
            recipients=email_list_formatted,
            subject=frappe._('E-Book geringe Menge'),
            header=('Der Bestand an E-Books ist gering'),
            template='e-book',
            args=dict(
                ebook_quantity=ebook_quantity
            )
        )


def __get_email_list__():
    email_list = frappe.db.get_single_value('Mietrecht Config', 'config')
    email_list_formatted = email_list.split(';')
    return email_list_formatted
