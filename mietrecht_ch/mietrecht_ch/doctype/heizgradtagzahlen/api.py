import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultRow import ResultRow

@frappe.whitelist(allow_guest=True)
def get_single_month(location, year, month):
    coldDays  = frappe.db.sql("""SELECT `monat` as `month`, `{location}` as `days`
                            FROM `tabHeizgradtagzahlen` 
                            WHERE `monat` LIKE '{date}';""".format(location=location, date=__buildFullDate(year, month)), as_dict=True)

    calculatorResult = CalculatorResult(coldDays[0] if coldDays else None, None)

    return CalculatorMasterResult(
        {'location':location, 'year':year, 'month':month},
        [calculatorResult]
    )

def __buildFullDate(year, month):
    return year + '-' + str.zfill(month, 2) + '-01'