from datetime import date

class HypoReferenzzinsDetail(dict):
    def __init__(self, date: date, interest: float, canton:str, since:date = None):
        dict.__init__(self, date=date, interest=interest, canton=canton, since=since)