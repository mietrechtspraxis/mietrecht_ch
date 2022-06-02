from typing import List
from numpy import number

FIELD_VALUE = 'value'
FIELD_PUBLISH_DATE = 'publish_date'
FIELD_BASE_YEAR = 'base_year'


class TeuerungIndex(dict):
    def __init__(self, requestedDate: str, value: float, affectedDate=None):
        dict.__init__(self, requestedDate=requestedDate,
                      value=value, affectedDate=affectedDate)


class TeuerungInflationResult(dict):
    def __init__(self, oldIndex: TeuerungIndex, newIndex: TeuerungIndex, inflation: float):
        dict.__init__(self, oldIndex=oldIndex,
                      newIndex=newIndex, inflation=inflation)


class MietzinsanpassungInflationResult(dict):
    def __init__(self, oldIndex: TeuerungIndex, newIndex: TeuerungIndex, inflation: float, calculation_variation: str, calculationRent: str):
        dict.__init__(self, oldIndex=oldIndex,
                      newIndex=newIndex, inflation=inflation, calculationRent=calculationRent, calculation_variation=calculation_variation)


class TeuerungLastRelevantIndexResult(dict):
    def __init__(self, basis: str, requestedDate: str, value: float, affectedDate: None):
        dict.__init__(self, basis=basis, requestedDate=requestedDate,
                      value=value, affectedDate=affectedDate)
