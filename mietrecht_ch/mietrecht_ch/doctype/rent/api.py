import json
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import DATE_FORMAT, buildDatesInChronologicalOrder
from mietrecht_ch.mietrecht_ch.doctype.teuerung.api import __get_values_from_sql_query__, __compute_result__
from mietrecht_ch.mietrecht_ch.doctype.hyporeferenzzins.api import __get_index_by_date__
from mietrecht_ch.models.rent import CalculationValue, Rent, UpdatedValue
from mietrecht_ch.utils.inflation import __rounding_value__
from mietrecht_ch.utils.hyporeferenzzinsUtils import __rent_pourcentage_calculation__


@frappe.whitelist(allow_guest=True)
def compute_rent():

    payload = json.loads(frappe.request.data)
    result = []
    rent = payload['rent']['rent']

    # Hypothekarzinsen
    fromYear = payload['hypoReference']['previous']['year']
    fromMonth = payload['hypoReference']['previous']['month']
    toYear = payload['hypoReference']['next']['year']
    toMonth = payload['hypoReference']['next']['month']
    canton: str = 'CH'

    old_date_formatted_hypo, new_date_formatted_hypo = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    # get data based on the old date
    get_index_from_date = __get_index_by_date__(
        canton, old_date_formatted_hypo, 1)
    # get data based on the new date
    get_index_to_date = __get_index_by_date__(
        canton, new_date_formatted_hypo, 1)

    from_date_interest = get_index_from_date[0].interest
    to_date_interest = get_index_to_date[0].interest

    rent_pourcentage_change = __rent_pourcentage_calculation__(
        from_date_interest, to_date_interest)

    calculation_rent_hypo = __rent_calculation__(rent, rent_pourcentage_change)

    result_hypothekarzinsen = CalculationValue(
        from_date_interest, to_date_interest, rent_pourcentage_change, calculation_rent_hypo)

    # Teuerung
    fromYear = payload['inflation']['previous']['year']
    fromMonth = payload['inflation']['previous']['month']
    toYear = payload['inflation']['next']['year']
    toMonth = payload['inflation']['next']['month']
    basis = payload['inflation']['basis']
    inflationRate: int = 100

    old_date_formatted_teuerung, new_date_formatted_teuerung = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted_teuerung, new_date_formatted_teuerung)

    teuerung_result = __compute_result__(
        inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, rent=None)
    teuerung_inflation = teuerung_result['inflation']
    calculation_rent_teuerung = __rent_calculation__(
        rent, teuerung_result['inflation'])
    rounded_calculation_rent_teuerung = __rounding_value__(
        calculation_rent_teuerung)

    results_teuerung = CalculationValue(
        teuerung_result['oldIndex']['value'], teuerung_result['newIndex']['value'], teuerung_inflation, rounded_calculation_rent_teuerung)

    # Total
    # total in percent from all calculation
    total_in_percent = teuerung_inflation + rent_pourcentage_change
    # total in sfr from all calculation
    total_in_sfr = calculation_rent_hypo + rounded_calculation_rent_teuerung

    # Mietzins
    original_rent = rent
    rent_updated_value = rent + total_in_sfr

    original_extra_room = payload['rent']['extraRoom']
    updated_extra_room = original_extra_room + total_in_sfr

    total_original = rent + original_extra_room
    total_updated = rent_updated_value + updated_extra_room
    round_total_updated = __rounding_value__(total_updated)

    result_mietzins = Rent(old_date_formatted_hypo, new_date_formatted_hypo, UpdatedValue(
        original_rent, rent_updated_value), UpdatedValue(original_extra_room, updated_extra_room), UpdatedValue(total_original, round_total_updated))
    return result_hypothekarzinsen, results_teuerung, result_mietzins,
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


def __rent_calculation__(rent, rent_pourcentage_change):
    return rent * rent_pourcentage_change / 100

# Get the Hypothekarzinsen result here
