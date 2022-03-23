import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.lebensdauer import FIELD_CHILD_OBJECT, FIELD_CHILDREN, FIELD_COMMENT, FIELD_LABEL, FIELD_LIFETIME, FIELD_OBJECT, LebensdauerEntry, LebensdauerRemedy, LebensdauerResult


@frappe.whitelist(allow_guest=True)
def get_all_by_group(groupId):

    groups: list = frappe.get_all(
        'LebensdauerGruppe',
        fields=[FIELD_LABEL, 'value'],
        filters={
            "value": ("like", groupId)
        }
    )

    if len(groups) == 0:
        return CalculatorMasterResult(
            {'groupId': groupId},
            [CalculatorResult(None, None)]
        )

    group = groups[0]

    groupObjects = frappe.get_all(
        'LebensdauerObjekte',
        fields=['*'],
        filters={
            "group": ("like", group.label)
        }
    )

    groupEntries = []

    __set_parents__(groupObjects, groupEntries)

    __set_children__(groupObjects, groupEntries)

    # We have to sort one more time, in case some fake parents have been added
    groupEntries.sort(key=lambda e: e[FIELD_LABEL])

    lebensdauerResult = LebensdauerResult(group.label, groupEntries)

    return CalculatorMasterResult(
        {'groupId': groupId},
        [CalculatorResult([lebensdauerResult], None)]
    )


def __set_children__(groupObjects, groupEntries):
    for child in sorted(filter(lambda o: o[FIELD_CHILD_OBJECT] and o[FIELD_CHILD_OBJECT] != '', groupObjects), key=lambda x: x[FIELD_CHILD_OBJECT]):
        __insert_child_object__(groupEntries, child)


def __insert_child_object__(groupEntries, obj):
    try:
        parent = next(
            x for x in groupEntries if x[FIELD_LABEL] == obj[FIELD_OBJECT])
    except StopIteration:
        # Parent was not found in database, we need to crerate a "fake" one
        parent = LebensdauerEntry(obj[FIELD_OBJECT])
        groupEntries.append(parent)

    if not parent[FIELD_CHILDREN]:
        parent[FIELD_CHILDREN] = []

    parent[FIELD_CHILDREN].append(LebensdauerEntry(
        obj[FIELD_CHILD_OBJECT], None, obj[FIELD_LIFETIME], __get_remedy__(obj), obj[FIELD_COMMENT]))


def __set_parents__(groupObjects, groupEntries):
    for parent in sorted(filter(lambda o: o[FIELD_CHILD_OBJECT] == '' or not o[FIELD_CHILD_OBJECT], groupObjects), key=lambda x: x[FIELD_OBJECT]):
        __insert_parent_object__(groupEntries, parent)


def __insert_parent_object__(groupEntries, obj):
    groupEntries.append(LebensdauerEntry(
        obj[FIELD_OBJECT], None, obj[FIELD_LIFETIME], __get_remedy__(obj), obj[FIELD_COMMENT]))


def __get_remedy__(obj):
    if (obj.remedy != None):
        return LebensdauerRemedy(obj['remedy'], obj['unit'], obj['price'])

    return None


@frappe.whitelist(allow_guest=True)
def get_all_by_keyword(keyword):

    groupObjects = frappe.get_all(
        'LebensdauerObjekte',
        fields=['*'],
        filters={
            "keywords": ("like", keyword)
        }
    )

    if len(groupObjects) == 0:
        structured_result = None

    return CalculatorMasterResult(
        {'keyword': keyword},
        [CalculatorResult(structured_result, None)]
    )