import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultRow import ResultRow
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_sum_for_month(location, year, month):
    coldDays  = execute_query("""SELECT `monat` as `month`, HEIZ.`cold_days` as `sum`
                                FROM `tabHeizgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE HEIZ.`monat` LIKE '{date}' AND LOC.`value` LIKE '{location}';""".format(location=location, date=buildFullDate(year, month)))
    
    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'year':year, 'month':month},
        [calculatorResult]
    )

@frappe.whitelist(allow_guest=True)
def get_sum_for_period(location, fromYear, fromMonth, toYear, toMonth):

    fromFull, toFull = buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth)

    coldDays  = execute_query("""SELECT HEIZ.`monat` as `month`, SUM(HEIZ.`cold_days`) as `sum`
                                FROM `tabHeizgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE LOC.`value` LIKE '{location}' AND HEIZ.`monat` BETWEEN '{fromFull}' AND '{toFull}';"""
                                .format(location=location, fromFull=fromFull, toFull=toFull))
    
    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'fromYear':fromYear, 'fromMonth':fromMonth, 'toYear':toYear, 'toMonth':toMonth},
        [calculatorResult]
    )

@frappe.whitelist(allow_guest=True)
def get_list_for_period(location, fromYear, fromMonth, toYear, toMonth):

    fromFull, toFull = buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth)
    
    coldDays  = execute_query("""SELECT HEIZ.`monat` as `month`, HEIZ.`cold_days` as `sum`
                                FROM `tabHeizgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE LOC.`value` LIKE '{location}' AND HEIZ.`monat` BETWEEN '{fromFull}' AND '{toFull}';"""
                                .format(location=location, fromFull=fromFull, toFull=toFull))

    resultTableDescriptions = [
        ResultTableDescription("Monat", "month"),
        ResultTableDescription("Jahr", "number"),
        ResultTableDescription("Tage", "number"),
    ]
    
    results = []
    if coldDays:
        for coldDay in coldDays:
            results.append(ResultRow([coldDay.month.month, coldDay.month.year, coldDay.sum]))

    resultTable = ResultTable(resultTableDescriptions, results)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {'location':location, 'fromYear':fromYear, 'fromMonth':fromMonth, 'toYear':toYear, 'toMonth':toMonth},
        [calculatorResult]
    )