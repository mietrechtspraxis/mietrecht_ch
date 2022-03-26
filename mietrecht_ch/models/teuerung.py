FIELD_VALUE = 'value'

class TeuerungOldIndex(dict):
    def __init__(self, oldIndexDate: float, value: float):
        dict.__init__(self, oldIndexDate=oldIndexDate, value=value)

class TeuerungNewIndex(dict):
    def __init__(self, newIndexDate: float, value: float):
        dict.__init__(self, newIndexDate=newIndexDate, value=value)

class TeuerungInflationResult(dict):
    def __init__(self, oldIndex: TeuerungOldIndex, newIndex: TeuerungNewIndex, inflation: float):
        dict.__init__(self, oldIndex=oldIndex,
                      newIndex=newIndex, inflation=inflation)
