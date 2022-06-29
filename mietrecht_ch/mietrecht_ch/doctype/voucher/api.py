from xxlimited import new
import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.utils.queryExecutor import execute_query
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult


VOUCHER_TABLE = 'Voucher'
PAK_TABLE = 'Pak'


@frappe.whitelist(allow_guest=True)
def get_voucher_informations(**kwargs):
    voucher_code = kwargs['voucher']
    email = kwargs['email']
    params = {"voucher": voucher_code, "email": email}
    voucher_doctype = frappe.get_doc(VOUCHER_TABLE, voucher_code)

    if voucher_doctype:
        voucher_name = voucher_doctype.name
        associated_pak = voucher_doctype.associated_pak
        if associated_pak:
            if email:
                __save_email_doctype__(email, voucher_doctype)
            results = {"voucher": voucher_name, "pak": associated_pak}
            return __calculator_master_result__(params, results)
        # return non_assigned_pak
        non_assigned_pak_value = __non_assigned_pak__()
        if email:
            __save_email_doctype__(email, voucher_doctype)
        __save_associated_pak_to_voucher__(
            voucher_doctype, non_assigned_pak_value)
        # update the relation in the pak table adding the value of the voucher
        __save_data_pak__(voucher_name, non_assigned_pak_value)
        results = {"voucher": voucher_name, "pak": non_assigned_pak_value}

    return __calculator_master_result__(params, results)


def __calculator_master_result__(params, results):
    calulatorResult = CalculatorResult(results, None)
    return CalculatorMasterResult(params, [calulatorResult])


def __save_associated_pak_to_voucher__(voucher_doctype, non_assigned_pak_value):
    voucher_doctype.associated_pak = non_assigned_pak_value
    voucher_doctype.save()


def __save_data_pak__(voucher_name, non_assigned_pak_value):
    pak_doctype = frappe.get_doc(PAK_TABLE, non_assigned_pak_value)
    pak_doctype.associated_voucher = voucher_name
    pak_doctype.save()


def __save_email_doctype__(email, voucher_doctype):
    voucher_doctype.email = email
    voucher_doctype.save()


def __non_assigned_pak__():
    non_assigned_pak = execute_query(
        """select * from tabPak where associated_voucher = '' or associated_voucher is null ORDER BY label DESC LIMIT 1""")
    non_assigned_pak_value = non_assigned_pak[0]['label']
    return non_assigned_pak_value


def update_doctype(doctype: str, doctype_name: str, options: dict):
    return frappe.db.set_value(doctype, doctype_name, options)
