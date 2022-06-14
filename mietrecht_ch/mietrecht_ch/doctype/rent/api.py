import json
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import DATE_FORMAT, buildDatesInChronologicalOrder, date_with_different_day, date_with_month_ahead
from mietrecht_ch.mietrecht_ch.doctype.teuerung.api import __get_values_from_sql_query__, __compute_result__
from mietrecht_ch.mietrecht_ch.doctype.hyporeferenzzins.api import __get_index_by_date__
from mietrecht_ch.models.rent import CalculationValue, Rent, UpdatedValue
from mietrecht_ch.utils.inflation import __rounding_value__
from mietrecht_ch.utils.hyporeferenzzinsUtils import __rent_pourcentage_calculation__


@frappe.whitelist(allow_guest=True)
def compute_rent():

    payload = json.loads(frappe.request.data)
    rent = payload['rent']['rent']

    # hypoReference
    old_date_formatted_hypo, new_date_formatted_hypo, from_date_interest, to_date_interest, rent_pourcentage_change, rounded_calculation_rent_hypo = hypotekarzins_data(
        payload, rent)

    result_hypothekarzinsen = CalculationValue(
        from_date_interest, to_date_interest, rent_pourcentage_change, rounded_calculation_rent_hypo)

    # Inflation
    teuerung_result, teuerung_inflation, rounded_calculation_rent_teuerung = teuerung_data(
        payload, rent)

    results_teuerung = CalculationValue(
        teuerung_result['oldIndex']['value'], teuerung_result['newIndex']['value'], teuerung_inflation, rounded_calculation_rent_teuerung)

    # Total
    # total in percent from all calculation
    total_in_percent = teuerung_inflation + rent_pourcentage_change
    rounded_total_in_percent = __rounding_value__(total_in_percent)
    # total in sfr from all calculation
    total_in_sfr = rounded_calculation_rent_hypo + rounded_calculation_rent_teuerung
    rounded_total_in_sfr = __rounding_value__(total_in_sfr)

    result_total = CalculationValue(
        '', '', rounded_total_in_percent, rounded_total_in_sfr)

    # Rent
    since_date, from_date, original_rent, rounded_updated_value, original_extra_room, rounded_updated_extra_room, total_original, round_total_updated = mietzins_data(
        payload, rent, old_date_formatted_hypo, new_date_formatted_hypo, total_in_sfr)

    result_mietzins = Rent(since_date, from_date, UpdatedValue(
        original_rent, rounded_updated_value), UpdatedValue(original_extra_room, rounded_updated_extra_room), UpdatedValue(total_original, round_total_updated))

    # Kostensteigerungen
    fromYear = payload['generalCostsIncrease']['previous']['year']
    fromMonth = payload['generalCostsIncrease']['previous']['month']
    toYear = payload['generalCostsIncrease']['next']['year']
    toMonth = payload['generalCostsIncrease']['next']['month']

    old_date_formatted, new_date_formatted = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)
    # Create function to get the last day
    start_day_date = date_with_different_day(old_date_formatted, 0)
    end_day_date = date_with_different_day(new_date_formatted, 28)

    return end_day_date

    # Big Result
    return result_mietzins, result_hypothekarzinsen, results_teuerung, result_total
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


def mietzins_data(payload, rent, old_date_formatted_hypo, new_date_formatted_hypo, total_in_sfr):
    # Mietzins
    since_date = old_date_formatted_hypo
    from_date = date_with_month_ahead(new_date_formatted_hypo, 1)

    original_rent = rent
    rent_updated_value = rent + total_in_sfr
    rounded_updated_value = __rounding_value__(rent_updated_value)

    original_extra_room = payload['rent']['extraRoom']
    updated_extra_room = original_extra_room + total_in_sfr
    rounded_updated_extra_room = __rounding_value__(updated_extra_room)

    total_original = rent + original_extra_room
    total_updated = rent_updated_value + updated_extra_room
    round_total_updated = __rounding_value__(total_updated)
    return since_date, from_date, original_rent, rounded_updated_value, original_extra_room, rounded_updated_extra_room, total_original, round_total_updated


def teuerung_data(payload, rent):
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
    if values_from_sql_query and len(values_from_sql_query) == 2:
        teuerung_result = __compute_result__(
            inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, rent=None)
        teuerung_inflation = teuerung_result['inflation']
        calculation_rent_teuerung = __rent_calculation__(
            rent, teuerung_result['inflation'])
        rounded_calculation_rent_teuerung = __rounding_value__(
            calculation_rent_teuerung)

        return teuerung_result, teuerung_inflation, rounded_calculation_rent_teuerung
    return frappe.throw('No data found for Inflation')


def hypotekarzins_data(payload, rent):
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

    if len(get_index_from_date and get_index_to_date) == 1:

        from_date_interest = get_index_from_date[0].interest
        to_date_interest = get_index_to_date[0].interest

        rent_pourcentage_change = __rent_pourcentage_calculation__(
            from_date_interest, to_date_interest)

        calculation_rent_hypo = __rent_calculation__(
            rent, rent_pourcentage_change)
        rounded_calculation_rent_hypo = __rounding_value__(
            calculation_rent_hypo)
        return old_date_formatted_hypo, new_date_formatted_hypo, from_date_interest, to_date_interest, rent_pourcentage_change, rounded_calculation_rent_hypo

    return frappe.throw('No Data for HypoReference')


def __rent_calculation__(rent, rent_pourcentage_change):
    return rent * rent_pourcentage_change / 100


class CustomException(Exception):
    """ my custom exception class """
