class CalculatorMasterResult(dict):
    def __init__(self, queryParams, calculatorResults) -> None:
        dict.__init__(self, queryParams=queryParams, calculatorResults=calculatorResults)