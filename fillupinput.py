#!/usr/local/bin/python

import datetime
import cgi;
import cgitb; cgitb.enable()  # for troubleshooting
import os;
import MileageDbInput
from decimal import *

os.environ['TZ'] = "US/Eastern"

def PrintHeaders():
	print "Content-Type: text/html" # HTML is following
	print # blank line, end of headers

def PrintShortHistory():
	print """
	<html>
	<head><title>Mileage Form Input</title>
	<style>
		input.standard {
			font-size: 110%;
		}
	</style>
	</head>
	<meta name="viewport" content="width=400, initial-scale=1.0, user-scalable=no"/>
	<meta name="format-detection" content="telephone=no">
	<body>
	  <h3> Mobile Mileage Form Input</h3>
	<table cellpadding="4" cellspacing="0" border="1">
		<tr><th>Date</th>
			<th>Miles</th><th>Gallons</th><th>Cost</th><th>Mileage</th>
		</tr>
	"""

	results = MileageDbInput.GetVehicleMaintenance(1, 5)

	for row in results:
		print "<tr>"
		print "<td><label title='%s'>%s</label></td>" % (row.date,
			row.date.strftime("%m/%d/%Y"))
		mileage = round(row.fillupmileage / row.fillupgallons, 2)
		print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
			% (round(row.fillupmileage, 1), row.fillupgallons, round(row.fillupcostpergallon, 2), mileage)
		print "</tr>"
		
	print "</table>"

def PrintFooter():
	print "</body></html>"

def PrintForm():
	today = datetime.datetime.today()
	print """
	  <form method="post" action="fillupinput.py">
		<input type="hidden" name="submitted" value="true"/>
		<p>Date: %s %s</p>
		<p>Miles: <input type="number" name="miles" autofocus step="0.1" class="standard"/></p>
		<p>Price: <input type="number" name="pricePerGallon" step="0.001" class="standard"/></p>
		<p>Gallons: <input type="number" name="gallons" step="0.001" class="standard"/></p>
		<p><input type="submit" value="Submit" /></p>
	  </form>""" % (today.date(), today.time().strftime("%H:%M"))

def Main():

	PrintHeaders()
	form = cgi.FieldStorage()
	submitted = form.getvalue("submitted", "")

	if submitted:
		date = datetime.datetime.today()
		miles = form.getvalue("miles", "")
		gallons = form.getvalue("gallons", "")
		pricePerGallon = form.getvalue("pricePerGallon", "")
		mileage = float(miles) / float(gallons)
		print """<p>Date: %s</p>
		<p>Mileage: %s</p>
		<p>Miles: %s</p>
		<p>Gallons: %s</p>
		<p>Price Per Gallon: %s</p>
		<p>Fill up Cost: %s</p>
		""" % (date, mileage, miles, gallons, pricePerGallon, 
			float(gallons) * float(pricePerGallon))

		result = MileageDbInput.InsertFillupRecord(date, Decimal(miles), 
			Decimal(gallons), Decimal(pricePerGallon))
		if result != None:
			print """<span style='color: red;'>ERROR %s</span>""" % result

	PrintShortHistory()
	print "<p/><a href=\"vehicleMaintenance.py\">Show Full history</a>"
	PrintForm()

Main()
