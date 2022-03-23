from unittest import result
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.queryExecutor import execute_query


@frappe.whitelist(allow_guest=True)
def get_dataset():

    db_objects = execute_query("""SELECT `date`, interest_rate, average FROM tabHypothekarzins
                                ORDER BY `date`
                                """)

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