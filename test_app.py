import unittest
from app.models import FillUp
from decimal import Decimal
from app import views
from flask import request, Flask
from tempfile import mkstemp
from flask.ext.zodb import ZODB
import os
import json

class TestApi(unittest.TestCase):

    def setUp(self):
        self.test_app = Flask(__name__)
        self.test_app.config.from_object('config')
        self.test_app.config["ZODB_STORAGE"] = "file://db/test_mileagedb.fs"
        self.db = ZODB(self.test_app)

    def tearDown(self):
        if os.path.isfile("db/test_mileagedb.fs"):
            os.remove("db/test_mileagedb.fs")
            os.remove("db/test_mileagedb.fs.index")
            os.remove("db/test_mileagedb.fs.lock")
            os.remove("db/test_mileagedb.fs.tmp")


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

        assert Decimal('2.539') == fu.price

    def test_VerifyPricesGreaterThan10Dollars(self):
        x = Decimal('12.53')
        fu = FillUp(price = x)

        assert Decimal('12.539') == fu.price

    def test_SubmitMileage_SavesNewSubmittion(self):
        form = {}
        form["miles"] = "123"
        form["price"] = "123"
        form["gallons"] = "123"
        form["latitude"] = ""
        form["longitude"] = ""
        with self.test_app.test_request_context(path='/submitMileage', data=form, method="POST"):
            result = json.loads(views.submitMileage().data)
            assert result["success"] == True
            tree = self.db["fillUps"]
            self.assertEqual(1, len(tree.keys()))
            minKey = tree.minKey()
            fu = tree[minKey]
            self.assertEqual(Decimal('123'), fu.gallons)

    @unittest.skip("Manual Test Only")
    def test_RequestHistoryWhenEmpty_ReturnsEmptyList(self):
        with self.test_app.test_request_context(path="/recentHistory"):
            views.recentHistory()
            #try:
            #    template = views.recentHistory()
            #except Exception, ex:
            #    self.fail("raised: {0}".format(ex))

            print(template)


if __name__ == '__main__':
    unittest.main()
        
