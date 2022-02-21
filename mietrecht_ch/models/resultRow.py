class ResultRow(dict):
    def __init__(self, values: list,  isSuperResult: bool = False) -> None:
        dict.__init__(self, values=values, isSuperResult=isSuperResult)