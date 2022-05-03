from datetime import datetime
from distutils.command.build import build
from numbers import Number
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.hypoReferenzzins import HypoReferenzzinsDetail, HypoReferenzzinsMortageInterest
from mietrecht_ch.models.teuerung import TeuerungIndex
from mietrecht_ch.utils.dateUtils import buildDatesInChronologicalOrder, buildFullDate
from mietrecht_ch.utils.queryExecutor import execute_query
from mietrecht_ch.utils.inflation import __round_inflation_number__
from mietrecht_ch.utils.hyporeferenzzinsUtils import __round_hypo_retourned_value__, __rent_pourcentage_calculation__, __custom_range__


KEY_AT = 'at'
KEY_FROM = 'from'
KEY_SINCE = 'since'
KEY_CANTON = 'canton'
KEY_DATE = 'date'
KEY_INTEREST = 'interest'


@frappe.whitelist(allow_guest=True)
def get_index_by_month(year: Number, month: Number, canton: str = 'CH'):

    request_date = buildFullDate(year, month)
    closest_index = __get_index_by_date__(canton, request_date, 2)

    result = None

    if len(closest_index) > 0:
        publish_date = str(closest_index[0].publish_date)

        if len(closest_index) == 1:
            result = __get_single_result(
                closest_index, request_date, publish_date)
        elif __published_at_beggining_of_the_month__(publish_date, request_date):
            result = __get_single_result(
                closest_index, request_date, publish_date)
        else:
            result = __get_double_result(closest_index, request_date)

    calculator_result = CalculatorResult(result, None)

    return CalculatorMasterResult(
        {'canton': canton, 'year': year, 'month': month},
        [calculator_result]
    )


@frappe.whitelist(allow_guest=True)
def get_interest_value_from_date(fromMonth: Number, fromYear: Number, toMonth: Number, toYear: Number, canton: str):

    requested_from_date, requested_to_date = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    get_index_from_date = __get_index_by_date__(canton, requested_from_date, 1)
    get_index_to_date = __get_index_by_date__(canton, requested_to_date, 1)

    result = None

    if len(get_index_from_date and get_index_to_date) == 1:
        affected_from_date = get_index_from_date[0].publish_date
        affected_to_date = get_index_to_date[0].publish_date

        from_date_interest = get_index_from_date[0].interest
        to_date_interest = get_index_to_date[0].interest

        rent_pourcentage_change = __rent_pourcentage_calculation__(
            from_date_interest, to_date_interest)

        result = HypoReferenzzinsMortageInterest(TeuerungIndex(requested_from_date, from_date_interest, None if str(requested_from_date) == str(affected_from_date) else affected_from_date), TeuerungIndex(
            requested_to_date, to_date_interest, None if str(requested_to_date) == str(affected_to_date) else affected_to_date), rent_pourcentage_change)

        Calculator_result = CalculatorResult(result, None)

        return CalculatorMasterResult(
            {'fromMonth': fromMonth, 'fromYear': fromYear,
                'toMonth': toMonth, 'toYear': toYear, 'canton': canton},
            [Calculator_result]
        )


@frappe.whitelist(allow_guest=True)
def get_mortgage_rate_table(canton: str):
    mortgage_rate_values = execute_query("""SELECT publish_date, interest FROM tabHypoReferenzzins
                            WHERE canton = '{canton}'
                            ORDER BY publish_date ASC
                            """.format(canton=canton))

    result = None

    if len(mortgage_rate_values) > 0:
        result = []
        array_date = __sorted_date__(mortgage_rate_values)
        for x in array_date:
            result.append([y for y in mortgage_rate_values if __get_year_from_date__(
                y['publish_date']) == x])

    result_table_description = [
        ResultTableDescription('Jahr', 'string'),
        ResultTableDescription('Monat', 'string'),
        ResultTableDescription('Zinssatz', 'string')
    ]

    result_table = ResultTable(result_table_description, result)

    calculator_result = CalculatorResult(None, result_table)

    return CalculatorMasterResult(
        {'canton': canton}, calculator_result
    )


def __sorted_date__(mortgage_rate_values):
    array_date = []
    for x in mortgage_rate_values:
        array_date.append(__get_year_from_date__(x['publish_date']))
    return sorted(set(array_date))


def __get_year_from_date__(date):
    datem = datetime.strptime(str(date), "%Y-%m-%d")
    year_of_date = datem.year
    return year_of_date


def __get_index_by_date__(canton, request_date, nbr_result):
    closest_index = execute_query("""SELECT publish_date, interest, canton 
                              FROM tabHypoReferenzzins 
                              WHERE (canton = '{canton}' OR canton = 'CH')
                              AND publish_date < LAST_DAY('{date}')
                              ORDER BY publish_date DESC
                              LIMIT {nbr_result}
                              """
                                  .format(canton=canton, date=request_date, nbr_result=nbr_result))

    return closest_index


def __get_double_result(closest_index, request_date):
    publish_date = str(closest_index[1].publish_date)
    return {
        KEY_AT: HypoReferenzzinsDetail(request_date, closest_index[1].interest, closest_index[1].canton, None if request_date == publish_date else publish_date),
        KEY_FROM: HypoReferenzzinsDetail(
            closest_index[0].publish_date, closest_index[0].interest, closest_index[0].canton)
    }


def __get_single_result(closest_index, request_date, publish_date):
    key = KEY_FROM if request_date == publish_date else KEY_AT
    return {
        key: HypoReferenzzinsDetail(
            request_date, closest_index[0].interest, closest_index[0].canton, None if request_date == publish_date else publish_date)
    }


def __published_at_beggining_of_the_month__(publish_date, request_date):
    return publish_date <= request_date
