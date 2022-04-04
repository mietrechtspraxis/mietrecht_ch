from datetime import date
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder
from mietrecht_ch.utils.queryExecutor import execute_query


@frappe.whitelist(allow_guest=True)
def get_dataset(fromMonth = '01', fromYear = '1970', toMonth = '12', toYear = str(date.today().year)):

    from_date, to_date = buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth, toDay='31')
    db_objects = execute_query("""SELECT `date`, interest_rate, average FROM tabHypothekarzins
                                WHERE `date` BETWEEN '{from_date}' AND '{to_date}'
                                ORDER BY `date`
                                """.format(from_date=from_date, to_date=to_date))

    next_update = execute_query("""SELECT `value` FROM tabSingles
                                WHERE `doctype` = 'Hypothekarzins Aktualisierungsdaten' and `field` = 'interest_rate_next_update'

                                """)

    return CalculatorMasterResult(
        {},
        [CalculatorResult(__build_dataset__(db_objects, next_update[0]['value']), None)]
    )

def __build_dataset__(db_objects, next_update):
    result = {
        'actualRate': 0,
        'nextUpdate': next_update,
        'labels': [],
        'rate': [],
        'average': []
    }
    result_length = len(db_objects)
    for i, object in enumerate(db_objects):
        result['labels'].append(object['date'])
        result['rate'].append(object['interest_rate'])
        result['average'].append(object['average'])
        if i == result_length - 1:
            result['actualRate'] = object['interest_rate']
    return result