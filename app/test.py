from decimal import *
import unittest
import MileageDbInput

class TestApi(unittest.TestCase):

	def setUp(self):
		self.api = MileageDbInput

	def test_PriceAutoAppends9(self):
		x = 1.10
		actual = self.api.addEnding9(x)

		self.assertEqual(Decimal('1.109'), actual)
	
	def test_PriceStaysSameIfAlreadyHasTrailing9(self):
		x = 1.109
		actual = self.api.addEnding9(x)

		self.assertEqual(Decimal(str(x)), actual)

	def test_VerifyFloatingPointArithmetic(self):
		x = 2.53
		actual = self.api.addEnding9(x)

		self.assertEqual(Decimal('2.539'), actual)

if __name__ == '__main__':
	unittest.main()
		
