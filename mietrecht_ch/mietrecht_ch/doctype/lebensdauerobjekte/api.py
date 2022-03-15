from ast import List
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.lebensdauer import LebensdauerEntry, LebensdauerRemedy, LebensdauerResult


@frappe.whitelist(allow_guest=True)
def get_all_by_group(groupId):

    groups: list = frappe.get_all(
        'LebensdauerGruppe',
        fields=['label', 'value'],
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

    parents = filter(lambda o : o['child_object'] == '', groupObjects)
    children = filter(lambda o : o['child_object'] != '', groupObjects)
    
    for obj in parents:
            __insert_parent_object__(groupEntries, obj)
    for obj in children:
            __insert_child_object__(groupEntries, obj)

    lebensdauerResult = LebensdauerResult(group.label, groupEntries)

    return CalculatorMasterResult(
        {'groupId': groupId},
        [CalculatorResult([lebensdauerResult], None)]
    )


def __insert_child_object__(groupEntries, obj):
    parent = next(x for x in groupEntries if x['label'] == obj['object'])

    if not parent['children']:
        parent['children'] = []

    parent['children'].append(__createEntry__(obj))


def __createEntry__(obj):
    return LebensdauerEntry(obj['object'], None, obj['lifetime'], __get_remedy__(obj), obj['comment'])


def __insert_parent_object__(groupEntries, obj):
    groupEntries.append(__createEntry__(obj))


def __get_remedy__(obj):
    if (obj.remedy != None):
        return LebensdauerRemedy(obj['remedy'], obj['unit'], obj['price'])

    return None


@frappe.whitelist(allow_guest=True)
def get_all_by_keyword(keyword):
    return CalculatorMasterResult(
        {'keyword': keyword},
        [CalculatorResult(get_fake_data(), None)]
    )


def get_fake_data():
    agregateChildren = [
        LebensdauerEntry('für Warmluftcheminée', lifetime=20),
        LebensdauerEntry('zur Wärmerückgewinnung', lifetime=20),
    ]

    chemineeChildren = [
        LebensdauerEntry('Cheminée, Cheminéeofen, Schwedenofen', lifetime=25),
        LebensdauerEntry('Schamottsteinauskleidung', lifetime=15,
                         remedy=LebensdauerRemedy('Neuauskleidung', 'm²', 800))
    ]

    chemineeEntries = [
        LebensdauerEntry('Aggregate', agregateChildren),
        LebensdauerEntry('Cheminéeabschluss',
                         comment="Metallgitter, Glas", lifetime=20),
        LebensdauerEntry('Cheminées', chemineeChildren),
        LebensdauerEntry('Ventilator', comment='Zu Rauchabzug', lifetime=20),
    ]

    otherChildren = [
        LebensdauerEntry('Kunststoft', lifetime=15,
                         remedy=LebensdauerRemedy('Ersatz', 'Stk.', 75)),
        LebensdauerEntry('Metall', lifetime=20,
                         remedy=LebensdauerRemedy('Ersatz', 'Stk.', 75)),
    ]

    otherEntries = [
        LebensdauerEntry(
            'Abdeckungen zu Lüftungsanlagen/-gittern', otherChildren),
    ]

    return [
        LebensdauerResult('Cheminée', chemineeEntries),
        LebensdauerResult('Heizung / Lüftung / Klima', otherEntries),
    ]
