import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_sum_for_month(location, year, month):
    coldDays  = execute_query("""SELECT `monat` as `month`, `{location}` as `sum`
                                FROM `tabHeizgradtagzahlen` 
                                WHERE `monat` LIKE '{date}';""".format(location=location, date=buildFullDate(year, month)))
    
    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'year':year, 'month':month},
        [calculatorResult]
    )

@frappe.whitelist(allow_guest=True)
def get_sum_for_period(location, fromYear, fromMonth, toYear, toMonth):

    fromFull, toFull = buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth)

    coldDays  = execute_query("""SELECT `monat` as `month`, SUM(`{location}`) as `sum`
                                FROM `tabHeizgradtagzahlen`
                                WHERE `monat` BETWEEN '{fromFull}' AND '{toFull}';"""
                                .format(location=location, fromFull=fromFull, toFull=toFull))
    
    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'fromYear':fromYear, 'fromMonth':fromMonth, 'toYear':toYear, 'toMonth':toMonth},
        [calculatorResult]
    )
