# python: 3.6.4.final.0
# pandas: 0.22.0

###################################
# Assumptions:
# 1) Transaction data provided to portVal as a pandas.DataFrame with columns
# 2) Simple PnL cacluation based on EoD position and averaged weigted price. No tranche accounting princial followed.
###################################

import config
import util
import pandas
import datetime

class portVal():

    def __init__(self, dfTrans, dictColMapping, dtValDate=None):
        self.dfTrans=dfTrans[list(dictColMapping.values())]
        self.valDate=util.getDate(dtValDate)
        self.dictColMapping=dictColMapping

    def builtPortfolio(self):
        dfPort=self.dfTrans[[dictColMapping['TradeDate'],dictColMapping['TradeDate']]]
        self.builtPortfolio=1

    def valuePortfolio(valDate=None):
        if valDate is not None:
            dfVal=self.dfTrans


def excludeFutureTrades(df, valDate):
    '''
    Filters DataFrame df by <= valDate to run EoD data cuts or avoid intra-day trades
    df as DataFrame containing transaction
    valDate
    '''
    return df[df.TradeDate<=valDate]