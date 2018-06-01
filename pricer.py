# python: 3.6.4.final.0

class pricer():
    """A class that prices instruments based on instrument id and date only.
       This is based on assumption that insturment id is unique and date is in not in future
    """

    def __init__(self, strInstID, dtValDate):
        self.instID=strInstID
        self.valDate=dtValDate

    def fetchPrice(self):
        return 1 #assumption made that price will be always available