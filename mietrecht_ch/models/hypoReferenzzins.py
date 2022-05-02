from mietrecht_ch.models.teuerung import TeuerungInflationResult, TeuerungIndex
from datetime import date
import numbers


class HypoReferenzzinsDetail(dict):
    def __init__(self, date: date, interest: float, canton: str, since: date = None):
        dict.__init__(self, date=date, interest=interest,
                      canton=canton, since=since)


class HypoReferenzzinsMortageInterest(dict):
    def __init__(self, oldIndex: TeuerungIndex, newIndex: TeuerungIndex, pourcentageChange: numbers):
        dict.__init__(self, oldIndex=oldIndex, newIndex=newIndex,
                      pourcentageChange=pourcentageChange)
