from decimal import *
import unittest
from models import FillUp
from decimal import Decimal

class TestApi(unittest.TestCase):

    def test_PriceAutoAppends9(self):
        x = Decimal('1.10')
        fu = FillUp(price = x)

        self.assertEqual(Decimal('1.109'), fu.price)
    
    def test_PriceStaysSameIfAlreadyHasTrailing9(self):
        x = Decimal('1.109')
        fu = FillUp(price = x)

        self.assertEqual(Decimal(str(x)), fu.price)

    def test_VerifyFloatingPointArithmetic(self):
        x = Decimal('2.53')
        fu = FillUp(price = x)

        self.assertEqual(Decimal('2.539'), fu.price)

    def test_VerifyPricesGreaterThan10Dollars(self):
        x = Decimal('12.53')
        fu = FillUp(price = x)

        assert Decimal('12.539') == fu.price


if __name__ == '__main__':
    unittest.main()
        
