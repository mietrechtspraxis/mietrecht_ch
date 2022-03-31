from typing import List
from numpy import number

FIELD_VALUE = 'value'

class TeuerungIndex(dict):
    def __init__(self, date: str, value: float):
        dict.__init__(self, date=date, value=value)

class TeuerungInflationResult(dict):
    def __init__(self, oldIndex: TeuerungIndex, newIndex: TeuerungIndex, inflation: float):
        dict.__init__(self, oldIndex=oldIndex,
                      newIndex=newIndex, inflation=inflation)

class TeuerungLastRelevantIndexResult(dict):
    def __init__(self, basis: str, fromMonth: number, fromYear: number):
        dict.__init__(self, basis=basis, fromMonth=fromMonth, fromYear=fromYear)