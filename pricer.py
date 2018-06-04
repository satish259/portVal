# python: 3.6.4.final.0

from unittest.mock import MagicMock

class pricer():
    """A class that gets prices for instruments based on instrument id and date only.
       This is based on assumption that insturment id is unique and date is in not in future
       A naive assumption made that prices come from the same system irrespective of instrument type
    """

    def __init__(self, strInstID, dtValDate):
        # Initialise class
        self.instID=strInstID # Instrment ID
        self.valDate=dtValDate # Valuation date
        self.gPrices={} # Global dictonary to hold fethed prices
        self.gConnection=MagicMock() #this establishes a connection to system to get price

    def fetchPrice(self):
        """ Check if price is in dictonary gPrices and returns it if present.
            Else calls getPrice to fetch price and adds to dictonary.
            Returns float
        """
        dKey= (str(self.valDate) +  ':' + str(self.instID))
        if dKey in self.gPrices:
            flPrice=self.gPrices[dKey]
        else:
            flPrice=self.getPrice()
            self.gPrices[dKey]=flPrice
        return flPrice

    def getPrice(self):
        """ Fetches price based valDate and instID. Mock used to ensure always avaialbe
            Returns float
        """
        with self.gConnection as gC:
            gC.price.return_value=1.0 #This is to account of price always being available 
            return gC.price(self.valDate, self.instID) # calls a function to get price for instrument and date

