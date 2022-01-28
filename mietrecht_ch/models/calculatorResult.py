class CalculatorResult(dict):
    def __init__(self, resultTitle, resultSubtitle, resultsTable) -> None:
        dict.__init__(self, resultTitle=resultTitle, resultSubtitle=resultSubtitle, resultsTable=resultsTable)