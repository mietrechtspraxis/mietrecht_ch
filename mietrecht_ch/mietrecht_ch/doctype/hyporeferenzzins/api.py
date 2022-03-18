from numbers import Number
from warnings import filters
import frappe
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_index_by_month(year: Number, month: Number, canton:str = 'CH'):
    
    print("Params : year:{} month:{} canton:{}".format(year, month, canton))
    
    result = execute_query("""SELECT canton, publish_date, interest 
                              FROM tabHypoReferenzzins 
                              WHERE (canton = '{canton}' OR canton = 'CH')
                              AND publish_date < LAST_DAY('{year}-{month}-01')
                              ORDER BY publish_date DESC
                              LIMIT 1
                              """
                              .format(canton=canton, year=year, month=month))
    
    return result