import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildFullDate
from pymysql import InternalError

log = frappe.logger("mietrecht.api")

@frappe.whitelist(allow_guest=True)
def get_single_month(location, year, month):
    coldDays = None
    try:
        coldDays  = frappe.db.sql("""SELECT `monat` as `month`, `{location}` as `days`
                                FROM `tabHeizgradtagzahlen` 
                                WHERE `monat` LIKE '{date}';""".format(location=location, date=buildFullDate(year, month)), as_dict=True)
    except InternalError:
       log.error('Heizgradtagzahlen Request Error', exc_info=True)

    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'year':year, 'month':month},
        [calculatorResult]
    )