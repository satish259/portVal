# python: 3.6.4.final.0

import dateutil.parser
import datetime
from pricer import pricer
from fxRates import fxRates

# This module contains reusable functions. The functions span a number of bespoke purposes

def getDate(dtIn):
    """ Function to parse date when string and to return datetime.date
        Returns today as date if no date provided, date was not parsed successfully or if date provided is in the future
    """
    dtOut=datetime.date.today()
    if dtIn is not None:
        try: 
            if isinstance(dtIn, datetime.datetime):
                dt=dtIn.date()
            elif isinstance(dtIn, datetime.date):
                dt=dtIn
            else:
                dt=dateutil.parser.parse(dtIn).date()
            if dt < datetime.date.today(): dtOut=dt
        except ValueError:
            pass
    return dtOut

def fetchPrice(strInstType, strInstID, dtValDate):
    """ Function to fetch price from pricer if stock or bond, else return 1 for cash
        returns float
    """
    dtValDate=getDate(dtValDate)
    if strInstType.upper() =='BOND' or strInstType.upper() =='STOCK':
        p1=pricer(strInstID, dtValDate)
        flOut=p1.fetchPrice()
    else:
        flOut=1 #cash does not have a price
    return flOut

def leftJoinDropColumns(dfLeft, dfRight, on):
    """ Sets index and joins two DataFrames and removes duplicate columns. Inndex reset on result to avoid calculational errors.
        This assumes that the column provided in 'on' is present in both DataFrames. 
        returns DataFrame
        Note this always performs as left join as the name suggests
    """
    for n in [dfLeft,dfRight]:
        if n.index.name is not None:
            n.reset_index(inplace=True)
        n.set_index(on,inplace=True)
    dfOut=dfLeft.join(dfRight,rsuffix='_r')
    dfOut.reset_index(inplace=True)
    return dfOut

def calcCost(dtValDate, flBaseValue, strPricingBasis, flCost, strBaseCCY, flTradeCount):
    """ Caclulates the cost of each trade position based on information provided.
        dtValDate is value date, strBaseCCY is ISO currency and strPricingBasis is % or ISO currency used for fx gate
        flBaseValue, flCost and flTradeCount are floats used to calculate cost of trade based on instrument type
        returns float
    """
    if strPricingBasis =='%':
        flOut=(abs(flBaseValue) * flCost)/100.0
    else:
        flOut=(flCost/fxRates(dtValDate, strBaseCCY, strPricingBasis).fetchFxRates()) * flTradeCount
    return flOut
