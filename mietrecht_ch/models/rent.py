# code for the Mietzinsanpassung incoming

class UpdatedValue(dict):
    def __init__(self, original: int, updated: int):
        dict.__init__(self, original=original, updated=updated)


class Rent(dict):
    def __init__(self, oldDate: str, newDate: str, rent: UpdatedValue, extraRooms: UpdatedValue, total: UpdatedValue):
        dict.__init__(self, oldDate=oldDate, newDate=newDate,
                      rent=rent, extraRooms=extraRooms, total=total)


class InflationCalculationValue(dict):
    def __init__(self, fromDate: int, at: int, percent: int, amount: int):
        dict.__init__(self, fromDate=fromDate, at=at,
                      percent=percent, amount=amount)


class CalculatedPercentage(dict):
    def __init__(self, percent: int, amount: int):
        dict.__init__(percent=percent, amount=amount)


class Justification(dict):
    def __init__(self, mortgageInterest: InflationCalculationValue, inflation: InflationCalculationValue, constIncrease: InflationCalculationValue, valueAdded: CalculatedPercentage, reserve: CalculatedPercentage, total: CalculatedPercentage):
        dict.__init__(mortgageInterest=mortgageInterest, inflation=inflation,
                      constIncrease=constIncrease, valueAdded=valueAdded, reserve=reserve, total=total)


class MortgageInterestRate(dict):
    def __init__(self, requestedDate: str, canton: int, value: int):
        dict.__init__(requestedDate=requestedDate, canton=canton, value=value)


class Inflation(dict):
    def __init__(self, requestedDate: str, percent: int, value: int, affectedDate: str):
        dict.__init__(requestedDate=requestedDate, percent=percent,
                      value=value, affectedDate=affectedDate)


class CostIncrease(dict):
    def __init__(self, flatRate: int, countedUpTo: str):
        dict.__init__(flatRate=flatRate, countedUpTo=countedUpTo)


class CostLevel(dict):
    def __init__(self, mortgageInterestRate: MortgageInterestRate, inflation: Inflation, costIncrease: CostIncrease):
        dict.__init__(mortgageInterestRate=mortgageInterestRate,
                      inflation=inflation, costIncrease=costIncrease)


class RentCalculatorResult(dict):
    def __init__(self, rent: Rent, justification: Justification, costLevel: CostLevel):
        dict.__init__(rent=rent,
                      justification=justification, costLevel=costLevel)
