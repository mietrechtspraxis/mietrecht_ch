import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultRow import ResultRow
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query
from mietrecht_ch.utils.validationUtils import data_empty_value
from mietrecht_ch.utils.validationTypeUtils import data_type_validation_str


@frappe.whitelist(allow_guest=True)
def get_single_oil_price(quantity, year, month):
    __validate_data__(quantity, year, month)
    oilPrice = frappe.get_all(
        'Heizolpreise',
        fields=[
            'monat as month',
            """{} as price""".format(quantity),
            """'{}' as quantity""".format(quantity)
        ],
        filters={
            "monat": ("like", buildFullDate(year, month))
        }
    )

    calculatorResult = CalculatorResult(
        oilPrice[0] if oilPrice else None, None)

    return CalculatorMasterResult(
        {'quantity': quantity, 'year': year, 'month': month},
        [calculatorResult]
    )


def __validate_data__(quantity, year, month):
    data_empty_value(month, 'month')
    data_type_validation_str(month, 'month')
    data_empty_value(year, 'year')
    data_type_validation_str(year, 'year')
    data_empty_value(quantity, 'quantity')
    data_type_validation_str(quantity, 'quantity')


@frappe.whitelist(allow_guest=True)
def get_multiple_oil_price(quantity, fromYear, fromMonth, toYear, toMonth):
    __validate_data_for_period__(
        quantity, fromYear, fromMonth, toYear, toMonth)
    fromFull, toFull = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)
    oilPrices = frappe.get_all(
        'Heizolpreise',
        fields=[
            'monat as month',
            """{} as price""".format(quantity),
            """'{} as quantity'""".format(quantity)
        ],
        filters=[
            ["monat", ">=", fromFull],
            ["monat", "<=", toFull],
        ],
        order_by='monat ASC'
    )

    resultTableDescriptions = [
        ResultTableDescription("Monat", "month"),
        ResultTableDescription("Jahr", "year"),
        ResultTableDescription("Preis in CHF", "number"),
    ]

    results = []
    if oilPrices:
        for oilPrice in oilPrices:
            results.append(
                ResultRow([oilPrice.month.month, oilPrice.month.year, oilPrice.price]))

    resultTable = ResultTable(resultTableDescriptions, results)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {'quantity': quantity, 'fromYear': fromYear,
            'fromMonth': fromMonth, 'toYear': toYear, 'toMonth': toMonth},
        [calculatorResult]
    )


def __validate_data_for_period__(quantity, fromYear, fromMonth, toYear, toMonth):

    data_empty_value(quantity, 'location')
    data_type_validation_str(quantity, 'location')
    data_empty_value(fromYear, 'fromYear')
    data_type_validation_str(fromYear, 'fromYear')
    data_empty_value(fromMonth, 'fromMonth')
    data_type_validation_str(fromMonth, 'fromMonth')
    data_empty_value(toYear, 'toYear')
    data_type_validation_str(toYear, 'toYear')
    data_empty_value(toMonth, 'toMonth')
    data_type_validation_str(toMonth, 'toMonth')


@frappe.whitelist(allow_guest=True)
def get_last_data_date():
    last_data_date = execute_query("""SELECT `monat` FROM tabHeizolpreise
                                    ORDER BY `monat` DESC 
                                    LIMIT 1
                                    """)
    return last_data_date[0]['monat'] if last_data_date else None
