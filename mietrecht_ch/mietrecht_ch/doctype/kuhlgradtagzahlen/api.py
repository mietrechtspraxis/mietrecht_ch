import frappe
from mietrecht_ch.utils.validationUtils import data_empty_value
from mietrecht_ch.utils.validationTypeUtils import data_type_validation_str
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_sum_for_month(location, year, month):
    
    __validate_data__(location, year, month)

    coldDays = execute_query("""SELECT `monat` as `month`, HEIZ.`hot_days` as `sum`
                                FROM `tabKuhlgradtagzahlen` AS HEIZ
                                JOIN `tabWetterstationen` AS LOC ON HEIZ.`location` = LOC.`label`
                                WHERE HEIZ.`monat` LIKE '{date}' AND LOC.`value` LIKE '{location}';""".format(location=location, date=buildFullDate(year, month)))

    calculatorResult = CalculatorResult(
        coldDays[0] if coldDays else None, None)

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
