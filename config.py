# python: 3.6.4.final.0
# pandas: 0.22.0

import pandas

def getTransFee():
    '''
    Returns a DataFrame that contains transaction fees to be used as a multiplier for transaction costs
    '''
    return pandas.DataFrame([['BOND','%',0.01],['STOCK','USD',5],['CASH','%',0]],columns=['InstrumentType','PricingBasis','Cost'])

def getBuySellMultipler():
    '''
    Returns a DataFrame that contains directional multiplier to work our PnL
    '''
    return pandas.DataFrame([['BUY',-1],['SELL',1]],columns=['Direction','Multiplier'])