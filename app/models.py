from decimal import Decimal
from time import strptime

class FillUp(object):
    def __init__(self, date = "", miles = 0, price = 0, gallons = 0, latitude = 0, longitude = 0):
        self._date = date
        self._miles = miles
        self._price = price    
        self._gallons = gallons 
        self._latitude = latitude 
        self._longitude = longitude

    @property
    def mileage(self):
        return round(self._miles / self._gallons, 2)

    @property
    def date(self):
        return self._date

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
        return round(self._latitude, 2)

    @property
    def longitude(self):
        return round(self._longitude, 2)

    def __repr__(self):
        return "{0} - {1} - {2} - {3}".format(self._date, self._miles, self._price, self._gallons)
