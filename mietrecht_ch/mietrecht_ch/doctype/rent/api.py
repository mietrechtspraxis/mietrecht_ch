from datetime import datetime
import json
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, date_with_different_day, date_with_month_ahead, buildFullDate
from mietrecht_ch.mietrecht_ch.doctype.teuerung.api import __get_values_from_sql_query__, __compute_result__
from mietrecht_ch.mietrecht_ch.doctype.hyporeferenzzins.api import __get_index_by_date__
from mietrecht_ch.models.rent import CalculationValue, CostIncrease, CostLevel, Inflation, Justification, MortgageInterestRate, Rent, RentCalculatorResult, UpdatedValue, CalculatedPercentage
from mietrecht_ch.utils.inflation import __rounding_value__
from mietrecht_ch.utils.hyporeferenzzinsUtils import __rent_pourcentage_calculation__
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
from mietrecht_ch.utils.inflation import __round_inflation_number__


@frappe.whitelist(allow_guest=True)
def compute_rent():

    payload = json.loads(frappe.request.data)
    rent = payload['rent']['rent']
    inflation_rate = 100
    canton = 'CH'

    # hypoReference
    from_interest, to_interest, rent_pourcentage_change, final_rent_hypo, old_date_formatted_hypo, new_date_formatted_hypo = hypotekarzins_data(
        payload, rent)

    result_hypothekarzinsen = CalculationValue(
        from_interest, to_interest, rent_pourcentage_change, final_rent_hypo)

    # Inflation
    # return teuerung_data(payload)
    from_index, at_index, teuerung_inflation, final_rent_calculation, index_basis, affected_date = teuerung_data(
        payload)
    results_teuerung = CalculationValue(
        from_index, at_index, teuerung_inflation, final_rent_calculation)

    # Kostensteigerungen
    start_day_date, end_day_date, cost_inflation, cost_value, flat_rate = general_costs_increase_data(
        payload, rent)
    return general_costs_increase_data(
        payload, rent)
    result_general_cost = CalculationValue(
        start_day_date, end_day_date, cost_inflation, cost_value)

    # Total
    # total in percent from all calculation
    rounded_total_in_percent, rounded_total_in_sfr = total_data(
        rent_pourcentage_change, final_rent_hypo, teuerung_inflation, final_rent_calculation, cost_inflation, cost_value)

    result_total = CalculatedPercentage(
        rounded_total_in_percent, rounded_total_in_sfr)

    # Rent
    since_date, from_date, original_rent, rounded_updated_value, original_extra_room, rounded_updated_extra_room, total_original, round_total_updated = mietzins_data(
        payload, rent, old_date_formatted_hypo, new_date_formatted_hypo, rounded_total_in_percent, rounded_total_in_sfr)

    # return rounded_updated_value

    result_mietzins = Rent(from_date, since_date, UpdatedValue(
        original_rent, rounded_updated_value), UpdatedValue(original_extra_room, rounded_updated_extra_room), UpdatedValue(total_original, round_total_updated))

    # CostLevel
    mortage_interest_rate = MortgageInterestRate(
        old_date_formatted_hypo, canton, from_interest)
    # Inflation
    data_inflation = Inflation(
        index_basis, inflation_rate, at_index, affected_date)

    # costIncrease
    cost_increase = CostIncrease(flat_rate, end_day_date)
    # Big Result
    results = result_mietzins, result_hypothekarzinsen, results_teuerung, result_general_cost, result_total, mortage_interest_rate, data_inflation, cost_increase

    calculatorResult = CalculatorResult(results, None)

    return CalculatorMasterResult(payload, RentCalculatorResult(result_mietzins, Justification(result_hypothekarzinsen, results_teuerung, result_general_cost, CalculatedPercentage(0, 0), CalculatedPercentage(0, 0), result_total), CostLevel(mortage_interest_rate, data_inflation, cost_increase)))
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
                "countedUpTo": "03-31-2022"
            }
        }
    }

    calculatorResult = CalculatorResult(data, None)

    return CalculatorMasterResult(
        payload,
        [calculatorResult]
    )


def total_data(rent_pourcentage_change, final_rent_hypo, teuerung_inflation, rent_teuerung, cost_inflation, cost_value):
    total_in_percent = teuerung_inflation + rent_pourcentage_change + cost_inflation
    rounded_total_in_percent = __rounding_value__(total_in_percent)
    # total in sfr from all calculation
    total_in_sfr = final_rent_hypo + \
        rent_teuerung + cost_value
    rounded_total_in_sfr = __rounding_value__(total_in_sfr)
    return rounded_total_in_percent, rounded_total_in_sfr


def general_costs_increase_data(payload, rent):
    fromYear = str(payload['generalCostsIncrease']['previous']['year'])
    fromMonth = str(payload['generalCostsIncrease']['previous']['month'])
    toYear = payload['generalCostsIncrease']['next']['year']
    toMonth = payload['generalCostsIncrease']['next']['month']
    flat_rate = payload['generalCostsIncrease']['flatRate']
    total_original = payload['rent']['rent'] + payload['rent']['extraRoom']

    old_date_formatted = buildFullDate(fromYear, fromMonth)
    new_date_formatted = buildFullDate(toYear, toMonth)

    # Create function to get the last day
    start_day_date = date_with_different_day(old_date_formatted, 1)
    end_day_date = date_with_different_day(new_date_formatted, 31)

    # Create new datetime parsed from a string
    new_start_date = datetime.strptime(start_day_date, "%Y-%m-%d")
    new_end_date = datetime.strptime(end_day_date, "%Y-%m-%d")

    # Start date in second
    start_seconds = get_seconds_from_date(new_start_date)

    # End date in second
    end_seconds = get_seconds_from_date(new_end_date)

    # Data calculation
    cost_inflation = round((end_seconds - start_seconds + 86400) /
                           (86400 * 30.4375), 0)/12

    cost_inflation = __rounding_value__(float(flat_rate) * cost_inflation)

    cost_value = __rounding_value__(total_original * cost_inflation * 0.01)
    return start_day_date, end_day_date, cost_inflation, cost_value, flat_rate


def get_seconds_from_date(date):
    start_date_in_second = date - datetime(1970, 1, 1)
    seconds = start_date_in_second.total_seconds()
    return seconds


def mietzins_data(payload, rent, old_date_formatted_hypo, new_date_formatted_hypo, rounded_total_in_percent, rounded_total_in_sfr):
    # Mietzins
    since_date = old_date_formatted_hypo
    from_date = date_with_month_ahead(new_date_formatted_hypo, 1)

    original_extra_room = payload['rent']['extraRoom']
    updated_extra_room = original_extra_room * rounded_total_in_percent * 0.01
    final_extra_room = updated_extra_room + original_extra_room
    rounded_updated_extra_room = __rounding_value__(final_extra_room)

    original_rent = rent
    rent_updated_value = rent * rounded_total_in_percent * 0.01
    finale_rent_updated_value = rent + rent_updated_value
    rounded_updated_value = __rounding_value__(finale_rent_updated_value)

    total_original = rent + original_extra_room
    total_updated = rounded_updated_value + rounded_updated_extra_room
    round_total_updated = __rounding_value__(total_updated)
    return since_date, from_date, original_rent, rounded_updated_value, original_extra_room, rounded_updated_extra_room, total_original, round_total_updated,


def teuerung_data(payload):
    # Teuerung
    fromYear = payload['inflation']['previous']['year']
    fromMonth = payload['inflation']['previous']['month']
    toYear = payload['inflation']['next']['year']
    toMonth = payload['inflation']['next']['month']
    basis = payload['inflation']['basis']
    total_original = payload['rent']['rent'] + payload['rent']['extraRoom']
    input_type = payload['inflation']['inputType']

    inflationRate: int = 40

    # old_date_formatted_teuerung, new_date_formatted_teuerung = buildDatesInChronologicalOrder(
    #     fromYear, fromMonth, toYear, toMonth)

    old_date_formatted_teuerung = buildFullDate(fromYear, fromMonth)
    new_date_formatted_teuerung = buildFullDate(toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted_teuerung, new_date_formatted_teuerung)
    index_basis = values_from_sql_query[1]['base_year']
    affected_date = values_from_sql_query[1]['publish_date']

    if input_type == 'search':
        return __get_data_from_search_input__(total_original, inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, index_basis, affected_date)
    return __get_data_from_manual_input__(payload, total_original, index_basis, affected_date)


def __get_data_from_search_input__(total_original, inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, index_basis, affected_date):

    if values_from_sql_query and len(values_from_sql_query) == 2:
        teuerung_result = __compute_result__(
            inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, rent=None)
        from_index = teuerung_result['oldIndex']['value']
        at_index = teuerung_result['newIndex']['value']
        teuerung_inflation = teuerung_result['inflation']
        calculation_rent_teuerung = __rent_calculation__(
            teuerung_result['inflation'], total_original)
        final_rent_calculation = __rounding_value__(
            calculation_rent_teuerung)

        return from_index, at_index, teuerung_inflation, final_rent_calculation, index_basis, affected_date
    raise BadRequestException('No data found for the inflation')


def __get_data_from_manual_input__(payload, total_original, index_basis, affected_date, inflation=100):
    from_index = payload['inflation']['previous']['index']
    at_index = payload['inflation']['next']['index']

    teuerung_inflation_not_rounded = __round_inflation_number__(
        from_index, at_index, inflation)
    teuerung_inflation = __rounding_value__(teuerung_inflation_not_rounded)

    calculation_rent_teuerung = __rent_calculation__(
        teuerung_inflation_not_rounded, total_original)
    final_rent_calculation = __rounding_value__(
        calculation_rent_teuerung)

    return from_index, at_index, teuerung_inflation, final_rent_calculation, index_basis, affected_date


def hypotekarzins_data(payload, rent):
    # Hypothekarzinsen

    fromYear = payload['hypoReference']['previous']['year']
    fromMonth = payload['hypoReference']['previous']['month']
    toYear = payload['hypoReference']['next']['year']
    toMonth = payload['hypoReference']['next']['month']
    total_original = payload['rent']['rent'] + payload['rent']['extraRoom']
    input_type = payload['hypoReference']['inputType']
    canton: str = 'CH'

    old_date_formatted_hypo, new_date_formatted_hypo = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    # old_date_formatted_hypo = buildFullDate(fromYear, fromMonth)
    # new_date_formatted_hypo = buildFullDate(toYear, toMonth)

    if input_type == 'search':
        return __get_data_hypo_from_search_input__(total_original, canton, old_date_formatted_hypo, new_date_formatted_hypo)
    return __get_data_hypoe_from_manual_input__(payload, total_original, old_date_formatted_hypo, new_date_formatted_hypo)


def __get_data_hypoe_from_manual_input__(payload, total_original, old_date_formatted_hypo, new_date_formatted_hypo):
    from_interest = payload['hypoReference']['previous']['rate']
    to_interest = payload['hypoReference']['next']['rate']

    rent_pourcentage_change = __rent_pourcentage_calculation__(
        from_interest, to_interest)
    calculation_rent_hypo = __rent_calculation__(
        total_original, rent_pourcentage_change)
    final_rent_hypo = __rounding_value__(
        calculation_rent_hypo)
    return from_interest, to_interest, rent_pourcentage_change, final_rent_hypo, old_date_formatted_hypo, new_date_formatted_hypo


def __get_data_hypo_from_search_input__(total_original, canton, old_date_formatted_hypo, new_date_formatted_hypo):
    # get data based on the old date
    get_index_from_date = __get_index_by_date__(
        canton, old_date_formatted_hypo, 1)
    # get data based on the new date
    get_index_to_date = __get_index_by_date__(
        canton, new_date_formatted_hypo, 1)

    if len(get_index_from_date and get_index_to_date) == 1:
        from_interest = get_index_from_date[0].interest
        to_interest = get_index_to_date[0].interest

        rent_pourcentage_change = __rent_pourcentage_calculation__(
            from_interest, to_interest)

        calculation_rent_hypo = __rent_calculation__(
            total_original, rent_pourcentage_change)
        final_rent_hypo = __rounding_value__(
            calculation_rent_hypo)
        return from_interest, to_interest, rent_pourcentage_change, final_rent_hypo, old_date_formatted_hypo, new_date_formatted_hypo
    raise BadRequestException('No data found for the mortgage interest.')


def __rent_calculation__(rent_pourcentage_change, total_original):
    return total_original * rent_pourcentage_change * 0.01
