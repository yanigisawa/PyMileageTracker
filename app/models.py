from decimal import Decimal

class FillUp(object):
    def __init__(self, date = "", miles = 0, price = 0, gallons = 0, latitude = 0, longitude = 0):
        self.date      = date
        self.miles     = miles
        self.price     = price    
        self.gallons   = gallons 
        self.latitude  = latitude 
        self.longitude = longitude

    @property
    def mileage(self):
        return Decimal(self.gallons) / Decimal(self.miles)
