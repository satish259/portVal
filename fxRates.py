# python: 3.6.4.final.0

from unittest.mock import MagicMock

class fxRates():
    """ A class that gets FX rates for date and base CCY
       This is based on assumption date is in not in future
    """

    def __init__(self, dtValDate, BaseCCY, ValueCCY):
        self.valDate=dtValDate # Valuation date
        self.BaseCCY=BaseCCY.upper() #  Base currency 
        self.ValueCCY=ValueCCY.upper() #The resulting currency (either USD or EUR for this exercise)
        self.gRates={} # Global dictonary to hold fethed FX rates
        self.gConnection=MagicMock() #this establishes a connection to system to get FX rates

    def fetchFxRates(self):
        """ Check if Fx Rates is in dictonary gRates and returns it if present.
            Else calls getFxRates to fetch rate.
        """
        dKey= (str(self.valDate) +  ':' + str(self.BaseCCY) +  ':' + str(self.ValueCCY))
        if dKey in self.gRates:
            dfRates=self.gRates[dKey]
        else:
            dfRates=self.getFxRates()
            self.gRates[dKey]=dfRates
        return dfRates
     
    def getFxRates(self):
        """ Fetches price based valDate. Mock used to ensure always avaialbe
            Returns float
            A naive assumption is made that xCCY is handled by the FxRates function
        """
        with self.gConnection as gC:
            gC.FxRates.return_value=1.0 #This is to account of rate always being available 
            return gC.FxRates(self.valDate, self.BaseCCY, self.ValueCCY) # calls a function to get price for currency and date