from numpy import number
from typing import List

FIELD_LABEL = 'label'
FIELD_CHILD_OBJECT = 'child_object'
FIELD_OBJECT = 'object'
FIELD_LIFETIME = 'lifetime'
FIELD_CHILDREN = 'children'
FIELD_COMMENT = 'comment'
FIELD_GROUP = 'group'

class LebensdauerRemedy(dict):
    def __init__(self, label:str, unit: str, price:number):
        dict.__init__(self, label=label, unit=unit, price=price)

class LebensdauerEntry(dict):
    def __init__(self, label, children: list = None, lifetime:number = None, remedy: LebensdauerRemedy = None, comment: str = None):
        dict.__init__(self, label=label, children=children, lifetime=lifetime, remedy=remedy, comment=comment)

class LebensdauerResult(dict):
    def __init__(self, groupName: str, entries: List[LebensdauerEntry]= None):
        dict.__init__(self, groupName=groupName, entries=entries)