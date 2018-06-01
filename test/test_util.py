import unittest
import datetime
import util

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

if __name__ == '__main__':
    unittest.main()
