from django.db import models

class Vehicle(models.Model):
	VIN = models.CharField("VIN", max_length=30)
	Make = models.CharField("Make", max_length=30)
	Model = models.CharField("Model", max_length=30)
	PurchaseDate = models.DateTimeField("Purchase Date")
	def __unicode__(self):
		return "VIN: %s - Make: %s - Model: %s" % (self.VIN, self.Make, self.Model)

class MaintenanceType(models.Model):
	name = models.CharField("Name", max_length=50)
	def __unicode__(self):
		return self.name


class VehicleMaintenance(models.Model):
	VehicleTypeId = models.ForeignKey(Vehicle)
	MaintenanceTypeId = models.ForeignKey(MaintenanceType)
	Date = models.DateTimeField("Date")
	Odometer = models.DecimalField("Odometer", decimal_places=2, max_digits=10)
	FillUpMileage = models.DecimalField("Miles", decimal_places=1, max_digits=10)
	FillUpGallons = models.DecimalField("Gallons", decimal_places=3, max_digits=10)
	FillUpCostPerGallon = models.DecimalField("Cost", decimal_places=3, max_digits=10)
	def __unicode__(self):
		return "Date: %s - Mileage: %s - Gallons: %s - Cost: %s" % (self.Date, self.FillUpMileage, self.FillUpGallons, self.FillUpCostPerGallon)

