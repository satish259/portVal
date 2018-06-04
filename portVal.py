# python: 3.6.4.final.0
# pandas: 0.22.0

###################################
# Assumptions:
# 1) Transaction data provided to portVal as a pandas.DataFrame with columns 'ValuationDate', 'InstrumentType', 'Direction', 'InstrumentID', 'Price', 'Nominal', 'BaseCCY'
# 2) Simple PnL cacluation based on EoD position and average price. No tranche accounting princial followed.
# 3) Assumption - Bond price is provided as CCY similar to stock
###################################

import config
import util
import pandas
import datetime
from fxRates import fxRates

class portVal():

    """ A class that caculates portfolio value, PnL (both realised and unrealised) on data provided as a DataFrame
        dfTrans is a DataFrame that contains transaction logs
        dictColMapping dictonary providing mapping to transaction log columns to required columns ['ValuationDate', 'InstrumentType', 'Direction', 'InstrumentID', 'Price', 'Nominal', 'BaseCCY'
        dtValDate is optional should historic valuation be required. Defaults to today. No future date allowed
        Returns a portVal object which contains underlying data and aggregated values
        Note: Sample file called 20180601.csv provided with project
        Possible function call portVal20180601 =portVal(pandas.from_csv(r'20180601.csv',{'Date': 'ValuationDate', 'InstType': 'InstrumentType', 'BuySell': 'Direction', 'InstID': 'InstrumentID', 'Price': 'Price', 'Nominal': 'Nominal', 'CCY': 'BaseCCY'})
    """    
    
    def __init__(self, dfTrans, dictColMapping, dtValDate=None):
        dtValDate=util.getDate(dtValDate)
        if dtValDate is None or dtValDate<datetime.date.today(): # check is value date is in the future
            raise ValueError('dtValDate cannot be None or in the future')
        dfTrans=dfTrans[list(dictColMapping.keys())]#removing columns that are not required from input 
        dfTrans.columns=list(dictColMapping.values()) #remapping columns based on m
        dfTrans['InstrumentType']=dfTrans['InstrumentType'].apply(lambda x: x.upper().strip())
        dfTrans['Direction']=dfTrans['Direction'].apply(lambda x: x.upper().strip())
        dfTrans['TradeCount']=dfTrans['ValuationDate']
        self.dictColMapping=dictColMapping 
        self.dfTrans=dfTrans
        self.dtValDate=dtValDate
        #runs functions defined below
        self.buildTransaction()
        self.valuePortfolio()
        self.runPnL()
        self.runPnLEnhanced()

    def buildTransaction(self):
        # Performs initial aggregation
        dfAgg=self.dfTrans[pandas.to_datetime(self.dfTrans['ValuationDate'],format="%d/%m/%Y" )<= self.dtValDate]#removed trades in the future
        dfAgg=dfAgg.groupby(['ValuationDate', 'InstrumentType', 'Direction', 'InstrumentID','BaseCCY'],as_index=False).agg({"Price":"mean","Nominal":"sum","TradeCount":"count"})
        dfAgg=util.leftJoinDropColumns(dfAgg,config.getBuySellMultipler(),'Direction')# Maps direction from config
        dfAgg=util.leftJoinDropColumns(dfAgg,config.getTransFee(),'InstrumentType') # Maps multipler from config
        dfAgg['BaseValue']=dfAgg['Price'] * dfAgg['Nominal'] * dfAgg['Multiplier']
        dfAgg['BaseCost']=dfAgg.apply(lambda row: util.calcCost(row['ValuationDate'],row['BaseValue'], row['PricingBasis'], row['Cost'], row['BaseCCY'], row['TradeCount']), axis=1)# calcuates cost
        dfAgg['Position']=-1.0 * dfAgg['Nominal'] * dfAgg['Multiplier']
        dfAgg['EodPrice']=dfAgg.apply(lambda row: util.fetchPrice(row['InstrumentType'], row['InstrumentID'], self.dtValDate), axis=1)#Gets prices for valuation day
        dfAgg['USDSpot']=dfAgg.apply(lambda row: fxRates(self.dtValDate, row['BaseCCY'], 'USD').fetchFxRates(), axis=1)#gets USD based rate for day
        dfAgg['EURSpot']=dfAgg.apply(lambda row: fxRates(self.dtValDate, row['BaseCCY'], 'EUR').fetchFxRates(), axis=1)#gets EUR based rate for day
        dfAgg['BaseValue']=(dfAgg['Position'] * dfAgg['EodPrice'])- dfAgg['BaseCost']
        dfAgg['PnL']=(dfAgg['Position'] * (dfAgg['EodPrice'] - dfAgg['Price']))- dfAgg['BaseCost']
        self.dfAggregated=dfAgg 

    def valuePortfolio(self):
        # Values portfolio based on instrument ID and provides a USD and EUR value
        dfVal=self.dfAggregated.groupby(['InstrumentID','USDSpot','EURSpot'],as_index=False).agg({"BaseValue":"sum"})
        self.dfValuation=dfVal
        self.USDValue=(dfVal['BaseValue'] * dfVal['USDSpot']).sum()
        self.EURValue=(dfVal['BaseValue'] * dfVal['EURSpot']).sum()

    def runPnL(self):
        # Calculates PnL as net balance * EoD price and provides a USD and EUR value
        dfPnL=self.dfAggregated.groupby(['InstrumentID','USDSpot','EURSpot'],as_index=False).agg({"PnL":"sum"})
        self.dfPnL=dfPnL
        self.USDPnL=(dfPnL['PnL'] * dfPnL['USDSpot']).sum()
        self.EURPnL=(dfPnL['PnL'] * dfPnL['EURSpot']).sum()

    def runPnLEnhanced(self):
        # Calculates oth realised and unrealised PnL and provides a USD and EUR value
        dfPnLe=self.dfAggregated.groupby(['Direction','InstrumentID','USDSpot','EURSpot','EodPrice'],as_index=False).agg({"Position":"sum","Price":"mean","BaseCost":"sum"})
        dfBuy=dfPnLe[dfPnLe['Direction']=='BUY']
        dfSell=dfPnLe[dfPnLe['Direction']=='SELL'][['InstrumentID','Position','Price']]
        dfSell.columns=['InstrumentID','SoldPosition','SoldPrice']
        dfPnLe=util.leftJoinDropColumns(dfBuy,dfSell,'InstrumentID').fillna(0)
        dfPnLe['RealisedPnL']=((dfPnLe['SoldPrice']-dfPnLe['Price'])*abs(dfPnLe['SoldPosition']))-dfPnLe['BaseCost']
        dfPnLe['UnrealisedPnL']=(dfPnLe['EodPrice']-dfPnLe['Price'])*(dfPnLe['Position']-dfPnLe['SoldPosition'])
        self.dfPnLenhanced=dfPnLe
        self.USDUnrealisedPnL=(dfPnLe['UnrealisedPnL'] * dfPnLe['USDSpot']).sum()
        self.EURUnrealisedPnL=(dfPnLe['UnrealisedPnL'] * dfPnLe['EURSpot']).sum()
        self.USDRealisedPnL=(dfPnLe['RealisedPnL'] * dfPnLe['USDSpot']).sum()
        self.EURRealisedPnL=(dfPnLe['RealisedPnL'] * dfPnLe['EURSpot']).sum()


