class ResultTableDescription(dict):
    def __init__(self, columnTitle, type) -> None:
        dict.__init__(self, columnTitle=columnTitle, type=type )