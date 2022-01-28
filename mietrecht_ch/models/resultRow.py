class ResultRow(dict):
    def __init__(self, type, values) -> None:
        dict.__init__(self, type=type, values=values)