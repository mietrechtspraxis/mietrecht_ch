from numbers import Number
from warnings import filters
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_index_by_month(year: Number, month: Number, canton:str = 'CH'):
    
    print("Params : year:{} month:{} canton:{}".format(year, month, canton))
    
    closestIndex = execute_query("""SELECT publish_date, interest 
                              FROM tabHypoReferenzzins 
                              WHERE (canton = '{canton}' OR canton = 'CH')
                              AND publish_date < LAST_DAY('{year}-{month}-01')
                              ORDER BY publish_date DESC
                              LIMIT 1
                              """
                              .format(canton=canton, year=year, month=month))
    result = None

    if len(closestIndex) > 0:
        result = {
            'interest' : {
                'publish_date': closestIndex[0].publish_date,
                'interest': closestIndex[0].interest
            }
        }
    
    calculatorResult = CalculatorResult(result, None)

    return CalculatorMasterResult(
        {'canton':canton, 'year':year, 'month':month},
        [calculatorResult]
    )