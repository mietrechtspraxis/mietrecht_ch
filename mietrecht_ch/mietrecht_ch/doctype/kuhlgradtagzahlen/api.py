import frappe
from mietrecht_ch.utils.validationUtils import data_empty_value
from mietrecht_ch.utils.validationTypeUtils import data_type_validation_str
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultRow import ResultRow
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.utils.dateUtils import buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, buildFullDate

@frappe.whitelist(allow_guest=True)
def get_sum_for_month(location, year, month):
    
    __validate_data__(location, year, month)

    hotDays = execute_query("""SELECT `monat` as `month`, HEIZ.`hot_days` as `sum`
                                FROM `tabKuhlgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE HEIZ.`monat` LIKE '{date}' AND LOC.`value` LIKE '{location}'
                                ;""".format(location=location, date=buildFullDate(year, month)))

    calculatorResult = CalculatorResult(
        hotDays[0] if hotDays else None, None)

    return CalculatorMasterResult(
        {'location': location, 'year': year, 'month': month},
        [calculatorResult]
    )

def __validate_data__(location, year, month):
    data_empty_value(month, 'month')
    data_type_validation_str(month, 'month')
    data_empty_value(year, 'year')
    data_type_validation_str(year, 'year')
    data_empty_value(location, 'location')
    data_type_validation_str(location, 'location')

@frappe.whitelist(allow_guest=True)
def get_sum_for_period(location, fromYear, fromMonth, toYear, toMonth):

    __validate_data_for_period__(
        location, fromYear, fromMonth, toYear, toMonth)

    fromFull, toFull = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    hotDays = execute_query("""SELECT HEIZ.`monat` as `month`, SUM(HEIZ.`hot_days`) as `sum`
                                FROM `tabKuhlgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE LOC.`value` LIKE '{location}' AND HEIZ.`monat` BETWEEN '{fromFull}' AND '{toFull}';"""
                             .format(location=location, fromFull=fromFull, toFull=toFull))

    calculatorResult = CalculatorResult(
        {'sum': hotDays[0].sum} if hotDays and hotDays[0] and hotDays[0].month else None, None)

    return CalculatorMasterResult(
        {'location': location, 'fromYear': fromYear,
            'fromMonth': fromMonth, 'toYear': toYear, 'toMonth': toMonth},
        [calculatorResult]
    )
    
@frappe.whitelist(allow_guest=True)
def get_list_for_period(location, fromYear, fromMonth, toYear, toMonth):

    __validate_data_for_period__(
        location, fromYear, fromMonth, toYear, toMonth)

    fromFull, toFull = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    hotDays = execute_query("""SELECT HEIZ.`monat` as `month`, HEIZ.`hot_days` as `sum`
                                FROM `tabKuhlgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE LOC.`value` LIKE '{location}' AND HEIZ.`monat` BETWEEN '{fromFull}' AND '{toFull}'
                                ORDER BY HEIZ.`monat`;"""
                             .format(location=location, fromFull=fromFull, toFull=toFull))

    resultTableDescriptions = [
        ResultTableDescription("Monat", "month"),
        ResultTableDescription("Jahr", "year"),
        ResultTableDescription("°C", "number"),
    ]

    results = []
    if hotDays:
        for coldDay in hotDays:
            results.append(
                ResultRow([coldDay.month.month, coldDay.month.year, coldDay.sum]))

    resultTable = ResultTable(resultTableDescriptions, results)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {'location': location, 'fromYear': fromYear,
            'fromMonth': fromMonth, 'toYear': toYear, 'toMonth': toMonth},
        [calculatorResult]
    )
    
    
def __validate_data_for_period__(location, fromYear, fromMonth, toYear, toMonth):

    data_empty_value(location, 'location')
    data_type_validation_str(location, 'location')
    data_empty_value(fromYear, 'fromYear')
    data_type_validation_str(fromYear, 'fromYear')
    data_empty_value(fromMonth, 'fromMonth')
    data_type_validation_str(fromMonth, 'fromMonth')
    data_empty_value(toYear, 'toYear')
    data_type_validation_str(toYear, 'toYear')
    data_empty_value(toMonth, 'toMonth')
    data_type_validation_str(toMonth, 'toMonth')


@frappe.whitelist(allow_guest=True)
def get_last_data_date():
    last_data_date = execute_query("""SELECT `monat` FROM tabHeizgradtagzahlen
                                    ORDER BY `monat` DESC 
                                    LIMIT 1
                                    """)
    return last_data_date[0]['monat'] if last_data_date else None
