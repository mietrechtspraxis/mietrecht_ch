from numbers import Number
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
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
    
    print("Params : year:{} month:{} canton:{}".format(year, month, canton))
    requestDate = buildFullDate(year, month)
    closestIndex = execute_query("""SELECT publish_date, interest, canton 
                              FROM tabHypoReferenzzins 
                              WHERE (canton = '{canton}' OR canton = 'CH')
                              AND publish_date < LAST_DAY('{date}')
                              ORDER BY publish_date DESC
                              LIMIT 2
                              """
                              .format(canton=canton, date=requestDate))

    result = None

    if len(closestIndex) > 0:
        publishDate = str(closestIndex[0].publish_date)

        if __published_at_beggining_of_the_month__(publishDate, requestDate) :
            result = __get_single_result(closestIndex, requestDate, publishDate)
        else :
            result = __get_double_result(closestIndex, requestDate)            
            
    
    calculatorResult = CalculatorResult(result, None)

    return CalculatorMasterResult(
        {'canton':canton, 'year':year, 'month':month},
        [calculatorResult]
    )

def __get_double_result(closestIndex, requestDate):
    publishDate = str(closestIndex[1].publish_date)
    return {
        KEY_AT: {
            KEY_SINCE: None if requestDate == publishDate else publishDate ,
            KEY_DATE: requestDate, 
            KEY_INTEREST: closestIndex[1].interest,
            KEY_CANTON: closestIndex[1].canton
        },
        KEY_FROM: {
            KEY_SINCE: None,
            KEY_DATE: closestIndex[0].publish_date, 
            KEY_INTEREST: closestIndex[0].interest,
            KEY_CANTON: closestIndex[0].canton
        }
    }

def __get_single_result(closestIndex, requestDate, publishDate):
    key = KEY_FROM if requestDate == publishDate else KEY_AT
    return {
        key : {
            KEY_SINCE: None if requestDate == publishDate else publishDate ,
            KEY_DATE: requestDate, 
            KEY_INTEREST: closestIndex[0].interest,
            KEY_CANTON: closestIndex[0].canton
        }
    }

def __published_at_beggining_of_the_month__(publishDate, requestDate):
    return publishDate < requestDate