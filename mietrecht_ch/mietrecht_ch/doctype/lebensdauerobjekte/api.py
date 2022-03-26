import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.lebensdauer import FIELD_CHILD_OBJECT, FIELD_CHILDREN, FIELD_COMMENT, FIELD_GROUP, FIELD_LABEL, FIELD_LIFETIME, FIELD_OBJECT, LebensdauerEntry, LebensdauerRemedy, LebensdauerResult
from mietrecht_ch.utils.queryExecutor import execute_query


@frappe.whitelist(allow_guest=True)
def get_all_by_group(groupId):

    db_objects = execute_query("""SELECT `tabObjects`.* FROM tabLebensdauerObjekte as tabObjects
                                    JOIN tabLebensdauerGruppe as tabGroup 
                                    ON tabObjects.group = tabGroup.label
                                    WHERE tabGroup.value = '{groupId}' 
                                    ORDER BY `group`, object, child_object
                                    """.format(groupId=groupId))

    return CalculatorMasterResult(
        {'groupId': groupId},
        [CalculatorResult(__build_structured_objects__(db_objects), None)]
    )

@frappe.whitelist(allow_guest=True)
def get_all_by_keyword(keyword):

    adapted_keyword = keyword.replace('*', '')
    db_objects = execute_query("""SELECT * FROM tabLebensdauerObjekte 
                                    WHERE (keywords LIKE {search} OR object LIKE {search} OR child_object LIKE {search} OR comment LIKE {search}) 
                                    ORDER BY `group`, object, child_object
                                    """.format(search="'%{}%'".format(adapted_keyword)))

    return CalculatorMasterResult(
        {'keyword': keyword},
        [CalculatorResult(__build_structured_objects__(db_objects), None)]
    )


def __get_lebendsauder_entry__(dbObject, isChild = False):
    return LebensdauerEntry(
        dbObject[FIELD_CHILD_OBJECT] if isChild  else dbObject[FIELD_OBJECT] , None, dbObject[FIELD_LIFETIME], __get_remedy__(dbObject), dbObject[FIELD_COMMENT])

def __get_remedy__(obj):
    if (obj.remedy != None):
        return LebensdauerRemedy(obj['remedy'], obj['unit'], obj['price'])

    return None

def __build_structured_objects__(db_objects):
    if not db_objects or len(db_objects) == 0:
        structured_objects = None
    
    else:
        structured_objects = []
        last_group = LebensdauerResult('')
        last_object = LebensdauerEntry('')
        for object in db_objects:
            if last_group['groupName'] != object[FIELD_GROUP]:
                last_group = LebensdauerResult(object[FIELD_GROUP])
                structured_objects.append(last_group)

            if last_object[FIELD_LABEL] != object[FIELD_OBJECT]:
                last_object = __get_lebendsauder_entry__(object)
                if not last_group['entries']: 
                    last_group['entries'] = [last_object]
                else:
                    last_group['entries'].append(last_object)

            if object[FIELD_CHILD_OBJECT] and object[FIELD_CHILD_OBJECT] != '':
                child_entry = __get_lebendsauder_entry__(object, True)
                if not last_object[FIELD_CHILDREN]:
                    last_object[FIELD_CHILDREN] = [child_entry]
                else:
                    last_object[FIELD_CHILDREN].append(child_entry)
    
    return structured_objects
