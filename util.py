# python: 3.6.4.final.0

import dateutil.parser
import datetime
from pricer import pricer

def getDate(dtIn):
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
    dtValDate=getDate(dtValDate)
    if strInstType.upper() =='BOND' or strInstType.upper() =='STOCK':
        p1=pricer(strInstID, dtValDate)
        flOut=p1.fetchPrice()
    else:
        flOut=1 #cash does not have a price
    return flOut

