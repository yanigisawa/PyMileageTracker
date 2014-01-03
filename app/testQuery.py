#!/usr/local/bin/python

import datetime
import cgi;
import cgitb; cgitb.enable()  # for troubleshooting
import os;
import MileageDbInput
from decimal import *
from django.conf import settings


settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
	DATABASES = {
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


os.environ['TZ'] = "US/Eastern"

def PrintHeaders():
	print "Content-Type: text/html" # HTML is following
	print # blank line, end of headers

def PrintShortHistory():
	print """
	<html>
	<head><title>Mileage Form Input</title></head>
	<meta name="viewport" content="width=400, initial-scale=1.0, user-scalable=no"/>
	<meta name="format-detection" content="telephone=no">
	<body>
	  <h3> Mobile Mileage Form Input</h3>
	<table cellpadding="4" cellspacing="0" border="1">
		<tr><th>Date</th>
			<th>Miles</th><th>Gallons</th><th>Cost</th><th>Mileage</th>
		</tr>
	"""

	results = Vehiclemaintenance.objects.all()[:5]

	for row in results:
		print "<tr>"
		print "<td><label title='%s'>%s</label></td>" % (row.date,
			row.date.strftime("%m/%d/%Y"))
		mileage = round(row.fillupgallons / row.fillupmileage, 2)
		print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
			% (round(row.fillupmileage, 1), row.fillupgallons, 
				round(row.fillupcostpergallon, 2), mileage)
		print "</tr>"
		
	print "</table>"

def PrintFooter():
	print "</body></html>"

def Main():

	PrintHeaders()
	form = cgi.FieldStorage()


	PrintShortHistory()

Main()
