#!/usr/local/bin/python

from decimal import *
from django.conf import settings

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
	DATABASES = {
		'prod': {
			'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			'NAME': 'jamesral_Mileage',                      # Or path to database file if using sqlite3.
			'USER': 'jamesral_mileage',                      # Not used with sqlite3.
			'PASSWORD': 'ivFrqoW9hIGcdzNdMYwV',                  # Not used with sqlite3.
			'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
			'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
		},
		'default': {
			'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			'NAME': 'mileage',                      # Or path to database file if using sqlite3.
			'USER': 'root',                      # Not used with sqlite3.
			'PASSWORD': 'root',                  # Not used with sqlite3.
			'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
			'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
		}
	})	

from mileage.models import *

def addEnding9(amount):
	newAmount = Decimal(str(amount))
	if len(str(newAmount)) <= 4:
		newAmount += Decimal('0.009')

	return newAmount		

def InsertFillupRecord(date, miles, gallons, pricePerGallon):
	pricePerGallon = addEnding9(pricePerGallon)
	vm = Vehiclemaintenance()
	vm.date = date
	v = Vehicle.objects.filter(pk=1)
	vm.vehicleid = v[0]
	mt = Maintenancetype.objects.filter(pk=1)
	vm.maintenancetypeid = mt[0]
	vm.fillupmileage = miles
	vm.fillupgallons = gallons
	vm.fillupcostpergallon = pricePerGallon
	vm.save()

def GetVehicleMaintenance(page, pageSize):
	stmt = """SELECT concat(concat( v.Make, " "), v.Model), mt.Name, Date, FillUpMileage, 
					 FillUpGallons, FillUpCostPerGallon 
			  FROM VehicleMaintenance vm
			  	JOIN Vehicle v on v.Id = vm.VehicleId
			  	JOIN MaintenanceType mt ON mt.Id = vm.MaintenanceTypeId
			  ORDER BY Date DESC
			  LIMIT %s, %s""" % (page, pageSize)

	startIndex = (page - 1) * pageSize
	endIndex = startIndex + pageSize
	return Vehiclemaintenance.objects.all().order_by('-date')[startIndex:endIndex]
