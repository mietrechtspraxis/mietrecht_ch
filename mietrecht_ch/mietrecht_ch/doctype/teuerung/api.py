from datetime import datetime, timedelta
from queue import Empty
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultRow import ResultRow
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.teuerung import MietzinsanpassungInflationResult, TeuerungInflationResult, TeuerungIndex, TeuerungLastRelevantIndexResult, FIELD_VALUE, FIELD_PUBLISH_DATE, FIELD_BASE_YEAR
from mietrecht_ch.utils.queryExecutor import execute_query
from mietrecht_ch.utils.dateUtils import DATE_FORMAT, buildFullDate, buildDatesInChronologicalOrder
from mietrecht_ch.utils.inflation import __round_inflation_number__, __rounding_value__
from mietrecht_ch.utils.validationUtils import data_empty_value
from mietrecht_ch.utils.validationTypeUtils import data_type_validation_str

from itertools import groupby

@frappe.whitelist(allow_guest=True)
def get_indexes_by_basis(basis):
    all_basis = frappe.get_all(
        'Teuerung',
        fields=['value', 'publish_date'],
        filters=[
            ['base_year', '=', basis]
        ],
        order_by='publish_date asc'
    )
    
    values = []
    for key, group in groupby(all_basis, key=lambda x: datetime.strptime(str(x['publish_date']), '%Y-%m-%d').year):
        value = {}
        indexes = list(group)
        value['year'] = key
        value['average'] = extract_average(indexes)
        value['indexes'] = indexes
        values.append(value)
        
    result = {'basis':basis, 'values': values}
    
    return result


def extract_average(indexes):
    average_value = None
    for item in reversed(indexes):
        if str(item['publish_date']).endswith("-12-31"):
            last_element = item
            average_value = last_element['value']
            item['average'] = last_element['value']
            indexes.remove(last_element)
                
    return average_value


@frappe.whitelist(allow_guest=True)
def get_all_basis():
    all_basis = frappe.get_all(
        'TeuerungBasis',
        fields=[FIELD_BASE_YEAR],
        order_by='base_year asc'
    )

    return all_data_gathered(all_basis)


def all_data_gathered(all_basis):
    results = []
    for x in all_basis:
        date_formatted = datetime.strftime(x[FIELD_BASE_YEAR], DATE_FORMAT)
        results.append({'value': date_formatted, 'label': x[FIELD_BASE_YEAR]})
    return results


@frappe.whitelist(allow_guest=True)
def get_last_five_indexes():

    last_five_publish_dates = execute_query(
        """select distinct(publish_date) from tabTeuerung where DAY(publish_date) = 1 order by publish_date desc LIMIT 5;""")
    last_five_publish_dates_reversed = last_five_publish_dates[::-1]

    inClause = ','.join(map(lambda x: "'{}'".format(
        x['publish_date'].strftime(DATE_FORMAT)), last_five_publish_dates))

    indexes = execute_query(
        """select base_year, publish_date, value from tabTeuerung where publish_date IN ({inClause}) order by base_year DESC, publish_date""".format(inClause=inClause))

    base_year_integer = []
    converted_base_year_integer = __create_unique_basis_from_indexes__(
        indexes, base_year_integer)

    result = []
    for x in converted_base_year_integer:
        listTemp = []
        listTemp.append(x)
        listTemp.extend([y['value']
                        for y in indexes if y[FIELD_BASE_YEAR] == str(x)])
        result.append(ResultRow(listTemp))

    result_table_description_iterated = [
        ResultTableDescription("auf der Basis", "string")]
    for x in last_five_publish_dates_reversed:
        result_table_description_iterated.append(
            ResultTableDescription(x['publish_date'], "number"))

    resultTable = ResultTable(result_table_description_iterated, result)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        None,
        [calculatorResult]
    )


@frappe.whitelist(allow_guest=True)
def get_inflation_for_period(basis: str, inflationRate: float, fromMonth: int, fromYear: int, toMonth: int, toYear: int):
    __data_validation__(basis, inflationRate, fromMonth,
                        fromYear, toMonth, toYear)
    old_date_formatted, new_date_formatted = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted, new_date_formatted)

    results = __compute_result__(
        inflationRate, old_date_formatted, new_date_formatted, values_from_sql_query)

    calculatorResult = CalculatorResult(results, None)

    return CalculatorMasterResult(
        {'basis': basis, 'inflationRate': inflationRate, 'fromMonth': fromMonth,
            'fromYear': fromYear, 'toMonth': toMonth, 'toYear': toYear},
        [calculatorResult]
    )


def __data_validation__(basis, inflationRate, fromMonth, fromYear, toMonth, toYear):
    data_empty_value(basis, 'basis')
    data_type_validation_str(basis, 'basis')
    data_empty_value(inflationRate, 'inflationRate')
    data_type_validation_str(inflationRate, 'inflationRate')
    data_empty_value(fromMonth, 'fromMonth')
    data_type_validation_str(fromMonth, 'fromMonth')
    data_empty_value(fromYear, 'fromYear')
    data_type_validation_str(fromYear, 'fromYear')
    data_empty_value(toMonth, 'toMonth')
    data_type_validation_str(toMonth, 'toMonth')
    data_empty_value(toYear, 'toYear')
    data_type_validation_str(toYear, 'toYear')


@frappe.whitelist(allow_guest=True)
def get_basis_by_index(index: int):
    all_basis = frappe.get_all(
        'Teuerung',
        fields=[FIELD_BASE_YEAR, 'publish_date'],
        filters=[
                ["value", "=", index]
        ]
    )

    results = __compute_all_basis_results__(all_basis, index)

    result_table_description = [
        ResultTableDescription('Basis', "year"),
        ResultTableDescription('Monat/Jahr', "month-year")
    ]

    resultTable = ResultTable(result_table_description, results)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {'index': index},
        [calculatorResult]
    )


@frappe.whitelist(allow_guest=True)
def get_last_index_from_basis(basis, fromMonth, fromYear):

    lastRelevant = __last_relevant_index_result__(basis, fromMonth, fromYear)

    results = lastRelevant[0] if len(lastRelevant) > 0 else None

    calculatorResult = CalculatorResult(results, None)

    return CalculatorMasterResult(
        {'basis': basis, 'fromMonth': fromMonth, 'fromYear': fromYear},
        [calculatorResult]
    )


@frappe.whitelist(allow_guest=True)
def get_rent_adjustment_data(rent, basis, inflationRate, fromMonth, fromYear, toMonth, toYear):

    old_date_formatted, new_date_formatted = buildDatesInChronologicalOrder(
        fromYear, fromMonth, toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted, new_date_formatted)

    results = __compute_result__(
        inflationRate, old_date_formatted, new_date_formatted, values_from_sql_query, rent)

    calculatorResult = CalculatorResult(results, None)

    return CalculatorMasterResult(
        {'rent': rent, 'basis': basis, 'inflationRate': inflationRate, 'fromMonth': fromMonth,
         'fromYear': fromYear, 'toMonth': toMonth, 'toYear': toYear},
        [calculatorResult]
    )


def __last_relevant_index_result__(basis, fromMonth, fromYear):

    date_formatted = buildFullDate(fromYear, fromMonth)

    relevant_date = __last_relevant_date__(date_formatted)

    last_relevant_index = execute_query(
        """select publish_date, base_year, value 
            from tabTeuerung 
            where base_year = '{basis}' and publish_date = '{relevant_date}'
            order by publish_date desc limit 1
            """
        .format(basis=basis, relevant_date=relevant_date))

    results = []
    if last_relevant_index and len(last_relevant_index) == 1:
        for i in last_relevant_index:
            results = [TeuerungLastRelevantIndexResult(
                i[FIELD_BASE_YEAR], date_formatted, i[FIELD_VALUE], None if str(date_formatted) == str(relevant_date) else relevant_date)]
    return results


def __compute_all_basis_results__(all_basis, index):
    results = None
    if index != '':
        results = []
        for b in all_basis:
            results.append(
                ResultRow([b[FIELD_BASE_YEAR], b[FIELD_PUBLISH_DATE]]))
    return results


def __compute_result__(inflationRate, old_date_formatted, new_date_formatted, values_from_sql_query, rent=None):
    results = None
    if values_from_sql_query and len(values_from_sql_query) == 2:
        old_index_value = values_from_sql_query[0][FIELD_VALUE]
        new_index_value = values_from_sql_query[1][FIELD_VALUE]
        affected_date = values_from_sql_query[1][FIELD_PUBLISH_DATE]

        calculation_inflation = __round_inflation_number__(
            old_index_value, new_index_value, inflationRate)

        if (rent != None):
            results = __result_of_all_data_with_rent__(old_date_formatted, new_date_formatted,
                                                       rent, old_index_value, new_index_value, affected_date, calculation_inflation)
        else:
            results = __result_of_all_data_without_rent__(
                old_date_formatted, old_index_value, new_date_formatted, new_index_value, calculation_inflation, affected_date)
    return results


def __get_values_from_sql_query__(basis, old_date_formatted, new_date_formatted):
    order = 'asc' if old_date_formatted < new_date_formatted else 'desc'
    relevant_date = __last_relevant_date__(new_date_formatted)

    sql = execute_query(
        """select base_year, publish_date, value
                from tabTeuerung 
                where base_year = '{basis}' and publish_date in ('{old_date_formatted}', '{relevant_date}')
                order by publish_date {order}"""
        .format(basis=basis, old_date_formatted=old_date_formatted, relevant_date=relevant_date, new_date_formatted=new_date_formatted, order=order))
    return sql


def __last_relevant_date__(new_date_formatted):
    last_relevant_date = execute_query("""select publish_date from tabTeuerung where publish_date <= '{new_date_formatted}' order by publish_date desc limit 1 """.format(
        new_date_formatted=new_date_formatted))
    value_last_relevant_date = last_relevant_date[0]['publish_date'] if last_relevant_date and len(
        last_relevant_date) > 0 else None
    return value_last_relevant_date


def __result_of_all_data_with_rent__(old_date_formatted, new_date_formatted, rent, old_index_value, new_index_value, affected_date, inflation):
    calculation_variation = __calculation_variation__(rent, inflation)
    rounded_calclulation_new_rent = __calculation_new_rent__(
        rent, calculation_variation)
    rounded_inflation = __rounding_value__(inflation)

    return MietzinsanpassungInflationResult(TeuerungIndex(old_date_formatted, old_index_value),
                                            TeuerungIndex(new_date_formatted, new_index_value, None if str(new_date_formatted) == str(affected_date) else affected_date), rounded_inflation, calculation_variation, rounded_calclulation_new_rent)


def __calculation_variation__(rent, rounded_inflation):
    calculation_variation = (int(rent) * rounded_inflation) / 100
    rounded_calculation_variation = __rounding_value__(calculation_variation)
    return rounded_calculation_variation


def __calculation_new_rent__(rent, calculation_variation):
    calculation_new_rent = int(rent) + calculation_variation
    rounded_calclulation_new_rent = __rounding_value__(calculation_new_rent)
    return rounded_calclulation_new_rent


def __result_of_all_data_without_rent__(old_date_formatted, old_index_value, new_date_formatted, new_index_value, inflation, affected_date):
    rounded_inflation = __rounding_value__(inflation)
    return TeuerungInflationResult(TeuerungIndex(old_date_formatted, old_index_value),
                                   TeuerungIndex(new_date_formatted, new_index_value, None if str(new_date_formatted) == str(affected_date) else affected_date), rounded_inflation)


def __create_unique_basis_from_indexes__(indexes, baseYearIntegers):
    for i in indexes:
        baseYearIntegers.append(i.base_year)
    return sorted(set(baseYearIntegers), key=None, reverse=True)
