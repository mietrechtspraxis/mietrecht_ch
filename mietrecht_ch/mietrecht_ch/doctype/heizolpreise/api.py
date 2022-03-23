import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultRow import ResultRow
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query

@frappe.whitelist(allow_guest=True)
def get_single_oil_price(quantity, year, month):
    oilPrice = frappe.get_all(
        'Heizolpreise', 
        fields = [
            'monat as month', 
            """{} as price""".format(quantity),
            """'{}' as quantity""".format(quantity)
            ], 
        filters = {
            "monat": ("like", buildFullDate(year, month))
        }
        )

    calculatorResult = CalculatorResult(oilPrice[0] if oilPrice else None, None)

    return CalculatorMasterResult(
        {'quantity':quantity, 'year':year, 'month':month},
        [calculatorResult]
    )

@frappe.whitelist(allow_guest=True)
def get_multiple_oil_price(quantity, fromYear, fromMonth, toYear, toMonth):

    fromFull, toFull = buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth)
    oilPrices = frappe.get_all(
        'Heizolpreise',
        fields = [
            'monat as month', 
            """{} as price""".format(quantity),
            """'{} as quantity'""".format(quantity)
            ], 
        filters = [
            ["monat", ">=", fromFull],
            ["monat", "<=", toFull],
        ],
        order_by = 'monat ASC'
    )
   
    resultTableDescriptions = [
        ResultTableDescription("Monat", "month"),
        ResultTableDescription("Jahr", "year"),
        ResultTableDescription("Preis in CHF", "number"),
    ]
    
    results = []
    if oilPrices:
        for oilPrice in oilPrices:
            results.append(ResultRow([oilPrice.month.month, oilPrice.month.year, oilPrice.price]))

    resultTable = ResultTable(resultTableDescriptions, results)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {'quantity':quantity, 'fromYear':fromYear, 'fromMonth':fromMonth, 'toYear':toYear, 'toMonth':toMonth},
        [calculatorResult]
    )
