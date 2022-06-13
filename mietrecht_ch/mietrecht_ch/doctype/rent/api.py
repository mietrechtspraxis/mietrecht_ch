import json
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import DATE_FORMAT, buildDatesInChronologicalOrder
from mietrecht_ch.mietrecht_ch.doctype.teuerung.api import __get_values_from_sql_query__, __compute_result__


@frappe.whitelist(allow_guest=True)
def compute_rent():

    payload = json.loads(frappe.request.data)

    # Teuerung
    fromYear = payload['inflation']['previous']['year']
    fromMonth = payload['inflation']['previous']['month']
    toYear = payload['inflation']['next']['year']
    toMonth = payload['inflation']['next']['month']
    basis = payload['inflation']['basis']
    inflationRate: int = 100

    old_date_formatted, new_date_formatted = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted, new_date_formatted)

    teuerung_result = __compute_result__(
        inflationRate, old_date_formatted, new_date_formatted, values_from_sql_query)

    return teuerung_result

    data = {
        "rent": {
            "since": "01-01-2022",
            "from": "06-01-2022",
            "rent": {
                "original": 1450.00,
                "updated": 1420.91
            },
            "extraRooms": {
                "original": 5.00,
                "updated": 0.91
            },
            "total": {
                "original": 1455.00,
                "updated": 1420.91
            }
        },
        "justification": {
            "mortgageInterest": {
                "from": 1.50,
                "at": 1.25,
                "percent": -2.91,
                "amount": -42.23
            },
            "inflation": {
                "from": 101.5,
                "at": 103.8,
                "percent": 0.91,
                "amount": 13.14
            },
            "constIncrease": {
                "from": "01-04-2018",
                "at": "31.03.2022",
                "percent": 4.32,
                "amount": 2.00
            },
            "valueAdded": {
                "percent": 0,
                "amount": 0
            },
            "reserve": {
                "percent": 0,
                "amount": 0
            },
            "total": {
                "percent": -2.01,
                "amount": -29.09
            }
        },
        "costLevel": {
            "mortgageInterestRate": {
                "requestedDate": "01-04-2022",
                "canton": "BS",
                "value": 1.25
            },
            "inflation": {
                "indexBasis": "01-05-2015",
                "percent": 100,
                "value": 103.8,
                "affectedDate": "01-03-2022"
            },
            "costIncrease": {
                "flatRate": 0.63,
                "countedUpTo": "31-03-2022"
            }
        }
    }

    calculatorResult = CalculatorResult(data, None)

    return CalculatorMasterResult(
        payload,
        [calculatorResult]
    )

# Get the Hypothekarzinsen result here
