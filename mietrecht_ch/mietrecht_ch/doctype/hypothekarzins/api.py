from datetime import date
from unittest import result
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder
from mietrecht_ch.utils.queryExecutor import execute_query


@frappe.whitelist(allow_guest=True)
def get_dataset(fromMonth = '01', fromYear = '1970', toMonth = '12', toYear = str(date.today().year)):

    from_date, to_date = buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth, toDay='31')
    print(from_date)
    print(to_date)
    db_objects = execute_query("""SELECT `date`, interest_rate, average FROM tabHypothekarzins
                                WHERE `date` BETWEEN '{from_date}' AND '{to_date}'
                                ORDER BY `date`
                                """.format(from_date=from_date, to_date=to_date))

    return CalculatorMasterResult(
        {},
        [CalculatorResult(__build_dataset__(db_objects), None)]
    )

def __build_dataset__(db_objects):
    result = {
        'labels': [],
        'rate': [],
        'average': []
    }
    for object in db_objects:
        result['labels'].append(object['date'])
        result['rate'].append(object['interest_rate'])
        result['average'].append(object['average'])
    return result