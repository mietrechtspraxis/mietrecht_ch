import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_single_month(location, year, month):
    coldDays  = execute_query("""SELECT `monat` as `month`, `{location}` as `days`
                                FROM `tabHeizgradtagzahlen` 
                                WHERE `monat` LIKE '{date}';""".format(location=location, date=buildFullDate(year, month)))
    
    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'year':year, 'month':month},
        [calculatorResult]
    )