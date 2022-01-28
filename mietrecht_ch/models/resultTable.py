class ResultTable(dict):
    def __init__(self, descriptions, results) -> None:
        dict.__init__(self, descriptions=descriptions, results=results )