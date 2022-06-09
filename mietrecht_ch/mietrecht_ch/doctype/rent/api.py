import json
import frappe
from mietrecht_ch.models.rent import TeuerungIndex
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult


@frappe.whitelist(allow_guest=True)
def compute_rent():

    # payload = json.loads(frappe.request.data)

    data = {
        "rent": {
            "netRent": {
                "inseredRent": 1450.00,
                "calculatedRent": 1420.91
            },
            "any": {
                "inseredRent": 5.00,
                "calculatedRent": 0.91
            },
            "totalRent": {
                "inseredRent": 1450.00,
                "calculatedRent": 1420.91
            }
        },
        "justification": {
            "mortgageInterest": {
                "from": 1.50,
                "at": 1.25,
                "pourcent": -2.91,
                "amount": -42.23
            },
            "inflation": {
                "from": 101.5,
                "at": 103.8,
                "pourcent": 0.91,
                "amount": 13.14
            },
            "constIncrease": {
                "from": "01-04-2018",
                "at": "31.03.2022",
                "pourcent": 4.32,
                "amount": 2.00
            },
            "valueAdded": {
                "pourcent": 3.27,
                "amount": 1.75
            },
            "reserve": {
                "pourcent": -2.01,
                "amount": -29.09
            }
        },
        "costLevel": {
            "mortgageInterestRate": {
                "requestedDate": "01-04-2022",
                "canton": 4051,
                "value": 1.25
            },
            "inflation": {
                "requestedDate": "01-05-2015",
                "pourcent": 100,
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
        None,
        [calculatorResult]
    )

# Get the Hypothekarzinsen result here
