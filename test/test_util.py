import unittest
import datetime
import util
import pandas

class Test_test_util(unittest.TestCase):
    def test_getDate(self):
        test1=util.getDate(datetime.date.today() + datetime.timedelta(days=1))
        test2=util.getDate(datetime.datetime(2018,5,31))
        test3=util.getDate('2018-05-31')
        test4=util.getDate(None)
        test5=util.getDate('this is not a real date')
        self.assertTrue(test1,datetime.date.today())
        self.assertTrue(test2,datetime.date(2018,5,31))
        self.assertTrue(test3,datetime.date(2018,5,31))
        self.assertTrue(test4,datetime.date.today())
        self.assertTrue(test5,datetime.date.today())
        
    def test_fetchPrice(self):
        test1=util.fetchPrice('bond','US46625H1005','2018-5-31')
        test2=util.fetchPrice('Stock','0925288','2018-5-31')
        test3=util.fetchPrice('CASH','USD','2018-5-31')
        self.assertTrue(test1,1)
        self.assertTrue(test2,1)
        self.assertTrue(test3,1)

    def test_leftJoinDropColumns(self):
        df1=pandas.DataFrame([['BUY',-1.0],['SELL',1.0]],columns=['Direction','Multiplier'])
        df2=pandas.DataFrame([['BUY',1.0],['SELL',-1.0]],columns=['Direction','Inverse'])
        test1=util.leftJoinDropColumns(df1,df2,'Direction')
        self.assertIsInstance(test1,pandas.DataFrame)

    def test_calcCost(self):
        test1=util.calcCost('2016-6-1',1.0,'USD',5.0,'USD',1)
        test2=util.calcCost('2016-6-1',1.0,'%',5.0,'USD',1)
        self.assertTrue(test1,5.0)
        self.assertTrue(test1,0.05)

if __name__ == '__main__':
    unittest.main()
