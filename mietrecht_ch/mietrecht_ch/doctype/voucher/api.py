from xxlimited import new
import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.utils.queryExecutor import execute_query

VOUCHER_TABLE = 'Voucher'
PAK_TABLE = 'Pak'


@frappe.whitelist(allow_guest=True)
def get_voucher_informations(**kwargs):
    voucher_code = kwargs['voucher']
    email = kwargs['email']

    voucher_doctype = frappe.get_doc(VOUCHER_TABLE, voucher_code)

    if voucher_doctype:
        voucher_name = voucher_doctype.name
        associated_pak = voucher_doctype.associated_pak
        if associated_pak:
            return voucher_doctype.associated_pak
        # return non_assigned_pak
        non_assigned_pak = execute_query(
            """select * from tabPak where associated_voucher = '' or associated_voucher is null ORDER BY label DESC LIMIT 1""")
        non_assigned_pak_value = non_assigned_pak[0]['label']

        if (email):
            voucher_doctype.associated_pak = non_assigned_pak_value
            voucher_doctype.email = email
            voucher_doctype.save()
        voucher_doctype.associated_pak = non_assigned_pak_value
        voucher_doctype.save()
        # update the relation in the pak table adding the value of the voucher
        pak_doctype = frappe.get_doc(PAK_TABLE, non_assigned_pak_value)
        pak_doctype.associated_voucher = voucher_name
        pak_doctype.save()

        return voucher_code.associated_pak


def update_doctype(doctype: str, doctype_name: str, options: dict):
    return frappe.db.set_value(doctype, doctype_name, options)
