from numpy import number
from typing import List


class LebensdauerRemedy(dict):
    def __init__(self, label:str, unit: str, price:number):
        dict.__init__(self, label, unit, price)

class LebensdauerEntry(dict):
    def __init__(self, label, children: list = None, lifetime:number = None, remedy: LebensdauerRemedy = None, comment: str = None):
        dict.__init__(self, label, children, lifetime, remedy, comment)

class LebensdauerResult(dict):
    def __init__(self, groupeName: str, entries: List[LebensdauerEntry]= None):
        dict.__init__(self, groupeName, entries)