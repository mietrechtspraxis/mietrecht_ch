import frappe
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultRow import ResultRow


@frappe.whitelist(allow_guest=True)
def get_single_oil_price(quantity, year, month):
    return frappe.db.sql("""SELECT `monat` as `month`, `{quantity}` as `price`, '{quantity}' as `quantity`
                            FROM `tabHeizolpreise` 
                            WHERE `monat` LIKE '{date}';""".format(quantity=quantity, date=__buildFullDate(year, month)), as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_multiple_oil_price(quantity, fromYear, fromMonth, toYear, toMonth):
    fromFull = __buildFullDate(fromYear, fromMonth)
    toFull = __buildFullDate(toYear, toMonth)

    #If user inverted the date, don't bother and just swap them
    if fromFull > toFull :
        toFull, fromFull = fromFull, toFull

    oilPrices = frappe.db.sql("""SELECT `monat` as `month`, `{quantity}` as `price`, '{quantity}' as `quantity`
                            FROM `tabHeizolpreise` 
                            WHERE `monat` BETWEEN '{fromFull}' AND '{toFull}' ;"""
                            .format(quantity=quantity, fromFull=fromFull, toFull=toFull), as_dict=True) 


    resultTableDescriptions = [
        ResultTableDescription("year", "number"),
        ResultTableDescription("month", "month"),
        ResultTableDescription("price", "number"),
    ]
    
    results = []

    for oilPrice in oilPrices:
        results.append(ResultRow('result', [oilPrice.month.year, oilPrice.month.month, oilPrice.price]))

    resultTable = ResultTable(resultTableDescriptions, results)

    calculatorResult = CalculatorResult('Liste der monatlichen Heizölpreise', '', resultTable)
    return {
        'queryParams': {'quantity':quantity, 'fromYear':fromYear, 'fromMonth':fromMonth, 'toYear':toYear, 'toMonth':toMonth},
        'calculatorResults':[calculatorResult]
    }

def __buildFullDate(year, month):
    return year + '-' + str.zfill(month, 2) + '-01'
