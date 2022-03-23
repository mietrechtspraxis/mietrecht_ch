from numbers import Number
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.hypoReferenzzins import HypoReferenzzinsDetail
from mietrecht_ch.utils.dateUtils import buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query

KEY_AT = 'at'
KEY_FROM = 'from'
KEY_SINCE = 'since'
KEY_CANTON = 'canton'
KEY_DATE = 'date'
KEY_INTEREST = 'interest'

@frappe.whitelist(allow_guest=True)
def get_index_by_month(year: Number, month: Number, canton:str = 'CH'):
    
    request_date = buildFullDate(year, month)
    closest_index = execute_query("""SELECT publish_date, interest, canton 
                              FROM tabHypoReferenzzins 
                              WHERE (canton = '{canton}' OR canton = 'CH')
                              AND publish_date < LAST_DAY('{date}')
                              ORDER BY publish_date DESC
                              LIMIT 2
                              """
                              .format(canton=canton, date=request_date))

    result = None

    if len(closest_index) > 0:
        publish_date = str(closest_index[0].publish_date)

        if __published_at_beggining_of_the_month__(publish_date, request_date) :
            result = __get_single_result(closest_index, request_date, publish_date)
        else :
            result = __get_double_result(closest_index, request_date)            
            
    
    calculator_result = CalculatorResult(result, None)

    return CalculatorMasterResult(
        {'canton':canton, 'year':year, 'month':month},
        [calculator_result]
    )

def __get_double_result(closest_index, request_date):
    publish_date = str(closest_index[1].publish_date)
    return {
        KEY_AT: HypoReferenzzinsDetail(request_date, closest_index[1].publish_date, closest_index[1].canton, None if request_date == publish_date else publish_date),
        KEY_FROM: HypoReferenzzinsDetail(closest_index[0].publish_date, closest_index[0].interest, closest_index[0].canton)
    }

def __get_single_result(closest_index, request_date, publish_date):
    key = KEY_FROM if request_date == publish_date else KEY_AT
    return {
        key : HypoReferenzzinsDetail(request_date, closest_index[0].publish_date, closest_index[0].canton, None if request_date == publish_date else publish_date)
    }

def __published_at_beggining_of_the_month__(publish_date, request_date):
    return publish_date < request_date