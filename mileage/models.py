# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	 * Rearrange models' order
#	 * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Dailymileage(models.Model):
	id = models.IntegerField(primary_key=True)
	miles = models.IntegerField(db_column='Miles') # Field name made lowercase.
	typeid = models.IntegerField(db_column='TypeId') # Field name made lowercase.
	createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
	mileagedate = models.DateTimeField(db_column='MileageDate') # Field name made lowercase.

	class Meta:
		db_table = u'DailyMileage'

	def __unicode__(self):
		return "Miles: %s - CreateDate: %s" % (self.miles, self.createdate)


class Maintenancetype(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=150, db_column='Name') # Field name made lowercase.

	class Meta:
		db_table = u'MaintenanceType'

	def __unicode__(self):
		return self.name


class Mileagetype(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=150, db_column='Name') # Field name made lowercase.
	class Meta:
		db_table = u'MileageType'

class Vehicle(models.Model):
	id = models.IntegerField(primary_key=True)
	vin = models.CharField(max_length=90, db_column='VIN', blank=True) 
	make = models.CharField(max_length=90, db_column='Make', blank=True) 
	model = models.CharField(max_length=90, db_column='Model', blank=True)
	purchasedate = models.DateTimeField(null=True, db_column='PurchaseDate', blank=True) 

	test = "foo"
	
	class Meta:
		db_table = u'Vehicle'

	def __unicode__(self):
		return u"VIN: %s - Make: %s - Model: %s" % (self.vin, self.make, self.model)


class Vehiclemaintenance(models.Model):
	id = models.IntegerField(primary_key=True)
	vehicleid = models.ForeignKey(Vehicle, db_column='VehicleId') # Field name made lowercase.
	maintenancetypeid = models.ForeignKey(Maintenancetype, db_column='MaintenanceTypeId') # Field name made lowercase.
	date = models.DateTimeField(db_column='Date') # Field name made lowercase.
	odometer = models.DecimalField(decimal_places=3, null=True, max_digits=22, 
		db_column='Odometer', blank=True) # Field name made lowercase.
	fillupmileage = models.DecimalField(decimal_places=3, null=True, max_digits=12, 
		db_column='FillUpMileage', blank=True) # Field name made lowercase.
	fillupgallons = models.DecimalField(decimal_places=3, null=True, max_digits=12, 
		db_column='FillUpGallons', blank=True) # Field name made lowercase.
	fillupcostpergallon = models.DecimalField(decimal_places=3, null=True, max_digits=12, 
		db_column='FillUpCostPerGallon', blank=True) # Field name made lowercase.

	class Meta:
		db_table = u'VehicleMaintenance'

	def __unicode__(self):
		return "Date: %s - Miles: %s - Cost: %s" % (self.date, self.fillupmileage, self.fillupcostpergallon)


