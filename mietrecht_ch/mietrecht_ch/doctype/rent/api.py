from datetime import datetime
import json
import re
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
from mietrecht_ch.utils.validationUtils import data_validation
from mietrecht_ch.utils.validationTypeUtils import data_type_validation_int, data_type_validation_str, data_type_validation_float, data_type_validation_float_and_int


@frappe.whitelist(allow_guest=True)
def compute_rent():

    payload = json.loads(frappe.request.data)
    rent = payload['rent']['rent']
    extra_room = payload['rent']['extraRoom']
    inflation_rate = 100
    canton = 'CH'

    __data_validation__(payload)

    # hypoReference
    from_interest, to_interest, rent_pourcentage_change, final_rent_hypo, old_date_formatted_hypo, new_date_formatted_hypo = hypotekarzins_data(
        payload, extra_room)

    result_hypothekarzinsen = CalculationValue(
        from_interest, to_interest, rent_pourcentage_change, final_rent_hypo)

    # Inflation
    from_index, at_index, teuerung_inflation, final_rent_calculation, index_basis, affected_date = teuerung_data(
        payload, extra_room)
    results_teuerung = CalculationValue(
        from_index, at_index, teuerung_inflation, final_rent_calculation)

    # Kostensteigerungen
    start_day_date, end_day_date, cost_inflation, cost_value, flat_rate = general_costs_increase_data(
        payload, extra_room)

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
        payload, rent, old_date_formatted_hypo, new_date_formatted_hypo, rounded_total_in_percent, rounded_total_in_sfr, extra_room)

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
    results = RentCalculatorResult(result_mietzins, Justification(result_hypothekarzinsen, results_teuerung, result_general_cost, CalculatedPercentage(
        0, 0), CalculatedPercentage(0, 0), result_total), CostLevel(mortage_interest_rate, data_inflation, cost_increase))

    calculatorResult = CalculatorResult(results, None)

    return CalculatorMasterResult(payload, [calculatorResult])


def total_data(rent_pourcentage_change, final_rent_hypo, teuerung_inflation, rent_teuerung, cost_inflation, cost_value):
    total_in_percent = teuerung_inflation + rent_pourcentage_change + cost_inflation
    rounded_total_in_percent = __rounding_value__(total_in_percent)
    # total in sfr from all calculation
    total_in_sfr = final_rent_hypo + \
        rent_teuerung + cost_value
    rounded_total_in_sfr = __rounding_value__(total_in_sfr)
    return rounded_total_in_percent, rounded_total_in_sfr


def general_costs_increase_data(payload, extra_room):
    fromYear = str(payload['generalCostsIncrease']['previous']['year'])
    fromMonth = str(payload['generalCostsIncrease']['previous']['month'])
    toYear = payload['generalCostsIncrease']['next']['year']
    toMonth = payload['generalCostsIncrease']['next']['month']
    flat_rate = payload['generalCostsIncrease']['flatRate']
    total_original = payload['rent']['rent'] + extra_room

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


def mietzins_data(payload, rent, old_date_formatted_hypo, new_date_formatted_hypo, rounded_total_in_percent, rounded_total_in_sfr, extra_room):
    # Mietzins
    since_date = old_date_formatted_hypo
    from_date = date_with_month_ahead(new_date_formatted_hypo, 1)

    original_extra_room = extra_room
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


def teuerung_data(payload, extra_room):
    # Teuerung
    fromYear = payload['inflation']['previous']['year']
    fromMonth = payload['inflation']['previous']['month']
    toYear = payload['inflation']['next']['year']
    toMonth = payload['inflation']['next']['month']
    basis = payload['inflation']['basis']
    total_original = payload['rent']['rent'] + extra_room
    input_type = payload['inflation']['inputType']
    inflation = payload['inflation']
    inflationRate: int = 40

    old_date_formatted_teuerung = buildFullDate(fromYear, fromMonth)
    new_date_formatted_teuerung = buildFullDate(toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted_teuerung, new_date_formatted_teuerung)

    if values_from_sql_query and len(values_from_sql_query) == 2:
        index_basis = values_from_sql_query[1]['base_year']
        affected_date = values_from_sql_query[1]['publish_date']

        if input_type == 'search':
            return __get_data_from_search_input__(total_original, inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, index_basis, affected_date)
        return __get_data_from_manual_input__(payload, total_original, index_basis, affected_date)
    raise BadRequestException('No data found for the inflation')


def __get_data_from_search_input__(total_original, inflationRate, old_date_formatted_teuerung, new_date_formatted_teuerung, values_from_sql_query, index_basis, affected_date):

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


def hypotekarzins_data(payload, extra_room):
    # Hypothekarzinsen

    fromYear = payload['hypoReference']['previous']['year']
    fromMonth = payload['hypoReference']['previous']['month']
    toYear = payload['hypoReference']['next']['year']
    toMonth = payload['hypoReference']['next']['month']
    total_original = payload['rent']['rent'] + extra_room
    input_type = payload['hypoReference']['inputType']
    hypo_reference = payload['hypoReference']
    canton: str = 'CH'

    old_date_formatted_hypo = buildFullDate(fromYear, fromMonth)
    new_date_formatted_hypo = buildFullDate(toYear, toMonth)

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


def __data_validation__(payload):

    __canton_validation__(payload)

    __rent_validation__(payload)

    __mortgage_validation__(payload)

    __inflation_validation__(payload)

    __general_cost_increase_validation__(payload)


def __general_cost_increase_validation__(payload):
    # general cost increase validation
    general_cost_increase = payload['generalCostsIncrease']
    flat_rate = general_cost_increase['flatRate']
    previous = general_cost_increase['previous']
    previous_month = previous['month']
    previous_year = previous['year']
    next = general_cost_increase['next']
    next_month = next['month']
    next_year = next['year']

    data_validation(general_cost_increase, 'generalCostsIncrease')
    data_validation(flat_rate, 'flat_rate')
    data_type_validation_float(flat_rate, 'flat_rate')
    data_validation(previous, 'previous')
    data_validation(previous_month, 'previous_month')
    data_type_validation_str(previous_month, 'previous_mont')
    data_validation(previous_year, 'previous_year')
    data_type_validation_str(previous_year, 'previous_year')
    data_validation(next, 'next')
    data_validation(next_month, 'next_month')
    data_type_validation_str(next_month, 'next_month')
    data_validation(next_year, 'next_year')
    data_type_validation_str(next_year, 'next_year')


def __inflation_validation__(payload):
    # Inflation validation
    inflation = payload['inflation']
    basis = inflation['basis']
    input_type = inflation['inputType']
    previous = inflation['previous']
    previous_month = previous['month']
    previous_year = previous['year']
    previous_index = previous['index']
    next = inflation['next']
    next_month = next['month']
    next_year = next['year']
    next_index = next['index']

    data_validation(inflation, 'inflation')
    data_validation(basis, 'basis')
    data_type_validation_str(basis, 'basis')
    data_validation(input_type, 'inputType')
    data_type_validation_str(input_type, 'input_type')
    data_validation(previous, 'previous')
    data_validation(previous_month, 'previous_month')
    data_type_validation_str(previous_month, 'previous_month')
    data_validation(previous_year, 'previous_year')
    data_type_validation_str(previous_year, 'previous_year')
    data_validation(previous_index, 'previous_index')
    data_type_validation_float_and_int(previous_index, 'previous_index')
    data_validation(next, 'next')
    data_validation(next_month, 'next_month')
    data_type_validation_str(next_month, 'next_month')
    data_validation(next_year, 'next_year')
    data_type_validation_str(next_year, 'next_year')
    data_validation(next_index, 'next_index')
    data_type_validation_float_and_int(next_index, 'next_index')


def __mortgage_validation__(payload):
    # Mortgage validation
    mortgage = payload['hypoReference']
    previous_mortgage = mortgage['previous']
    previous_month = previous_mortgage['month']
    previous_year = previous_mortgage['year']
    previous_rate = previous_mortgage['rate']
    next_mortage = mortgage['next']
    next_month = next_mortage['month']
    next_year = next_mortage['year']
    next_rate = next_mortage['rate']
    input_type = mortgage['inputType']

    data_validation(mortgage, 'mortgage')
    data_validation(previous_mortgage, 'previous')
    data_validation(previous_month, 'previous_month')
    data_type_validation_str(previous_month, 'previous_month')
    data_validation(previous_year, 'previous_year')
    data_type_validation_str(previous_year, 'previous_year')
    data_validation(previous_rate, 'previous_rate')
    data_type_validation_float(previous_rate, 'previous_rate')
    data_validation(next_mortage, 'next')
    data_validation(next_month, 'next_month')
    data_type_validation_str(next_month, 'next_mont')
    data_validation(next_year, 'next_year')
    data_type_validation_str(next_year, 'next_year')
    data_validation(next_rate, 'next_rate')
    data_type_validation_float(next_rate, 'next_rate')
    data_validation(input_type, 'inputType')
    data_type_validation_str(input_type, 'input_type')


def __rent_validation__(payload):
    # Rent validation
    rent = payload['rent']
    rent_rent = rent['rent']
    extra_room = payload['rent']['extraRoom']
    data_validation(rent, 'rent')
    data_validation(rent_rent, 'rent_rent')
    data_type_validation_int(rent_rent, 'rent_rent')
    data_validation(extra_room, 'extra_room')
    data_type_validation_int(extra_room, 'extra_room')


def __canton_validation__(payload):
    # Canton validation
    canton = payload['canton']
    data_validation(canton, 'canton')
    data_type_validation_str(canton, 'canton')
