class CalculatorResult(dict):
    def __init__(self, result, resultsTable) -> None:
        dict.__init__(self, result=result, resultsTable=resultsTable)