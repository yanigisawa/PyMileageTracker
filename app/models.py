from decimal import Decimal

class FillUp(object):
    def __init__(self, date = "", miles = 0, price = 0, gallons = 0, latitude = 0, longitude = 0):
        self._date      = date
        self._miles     = miles
        self._price     = price    
        self._gallons   = gallons 
        self._latitude  = latitude 
        self._longitude = longitude

    @property
    def mileage(self):
        return Decimal(self.gallons) / Decimal(self.miles)

    @property
    def date(self):
        return self._date.date()

    @property
    def miles(self):
        return self._miles

    @property
    def price(self):
        return self._price

    @property
    def gallons(self):
        return self._gallons
    
    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude
