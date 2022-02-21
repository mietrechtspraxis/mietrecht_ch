class CalculatorMasterResult(dict):
    def __init__(self, queryParams, calculatorResult) -> None:
        dict.__init__(self, queryParams=queryParams, calculatorResult=calculatorResult)