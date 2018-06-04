# python: 3.6.4.final.0
# pandas: 0.22.0

import pandas

# This module contains configeration as functions. The functions span a number of bespoke purposes

def getTransFee():
    '''
    Returns a DataFrame that contains transaction fees to be used as a multiplier for transaction costs
    '''
    return pandas.DataFrame([['BOND','%',0.01],['STOCK','USD',5.0],['CASH','%',0.0]],columns=['InstrumentType','PricingBasis','Cost'])

def getBuySellMultipler():
    '''
    Returns a DataFrame that contains directional multiplier to work our PnL
    '''
    return pandas.DataFrame([['BUY',-1.0],['SELL',1.0]],columns=['Direction','Multiplier'])