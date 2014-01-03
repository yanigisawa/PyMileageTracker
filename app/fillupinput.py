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
    print """
    <head><title>Mileage Form Input</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
    <meta name="format-detection" content="telephone=no">
    <link rel="apple-touch-icon" href="mileage_thumb.jpg" />
    <script src="js/geo.js" type="text/javascript" charset="utf-8"></script>
	<script src="http://code.jquery.com/jquery-1.6.4.min.js"></script>
    <script src="js/helpers.js" type="text/javascript" charset="utf-8"></script>
    <script src="js/jquery.validate.min.js" type="text/javascript" ></script>
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0.1/jquery.mobile-1.0.1.min.css" />
	<script src="http://code.jquery.com/mobile/1.0.1/jquery.mobile-1.0.1.min.js"></script>
    </head>
    <body>
    <div data-role="page">
        <div data-role="header">
		<h1>Maintenance Input</h1>
        </div>
    <div data-role="content">
    """

def PrintShortHistory():
    print """
    <table cellpadding="4" cellspacing="0" border="1" width="100%">
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
    print """
    <script type="text/javascript">
        $(document).ready(function () {
            Mileage.InitializePage();
        });

    </script>
    </div>
    </div>
    </body></html>
    """

def GetMaintenanceOptions():
    types = MileageDbInput.GetMaintenanceTypes()
    optionsStr = ""
    for t in types:
        optionsStr += ("<option value=\"%s\">%s</option>" % (t.id, t.name))

    return optionsStr

def PrintForm():
    today = datetime.datetime.today()
    print """
      <form id="mainForm" method="post" action="fillupinput.py">
        <input type="hidden" name="submitted" value="true"/>
        <p>Date: %s %s</p>
        <p>Type <select id="maintenanceTypes">%s</select>
        <p class="Fill-up">Miles: <input type="number" name="miles" autofocus step="0.1" class="standard required"/></p>
        <p class="Fill-up">Price: <input type="number" name="pricePerGallon" step="0.001" class="standard required"/></p>
        <p class="Fill-up">Gallons: <input type="number" name="gallons" step="0.001" class="standard required"/></p>
        <p class="Other">Odometer: <input type="number" name="odometer" step="0.1" class="standard required"/></p>
        <p><input type="submit" value="Submit" /></p>
        <input type="hidden" name="latitude" value="" />
        <input type="hidden" name="longitude" value="" />
      </form>""" % (today.date(), today.time().strftime("%H:%M"), GetMaintenanceOptions())

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
        latitude = form.getvalue("latitude", "")
        longitude = form.getvalue("longitude", "")
        print """<p>Date: %s</p>
        <p>Mileage: %s</p>
        <p>Miles: %s</p>
        <p>Gallons: %s</p>
        <p>Price Per Gallon: %s</p>
        <p>Fill up Cost: %s</p>
        <p>Latitude: %s</p>
        <p>Longitude: %s</p>
        """ % (date, mileage, miles, gallons, pricePerGallon, 
            float(gallons) * float(pricePerGallon), latitude, longitude)

        result = MileageDbInput.InsertFillupRecord(date, Decimal(miles), 
            Decimal(gallons), Decimal(pricePerGallon), latitude, longitude)
        if result != None:
            print """<span style='color: red;'>ERROR %s</span>""" % result

    PrintShortHistory()
    print "<p/><a href=\"vehicleMaintenance.py\">Show Full history</a>"
    if not submitted: PrintForm();
    PrintFooter()

Main()
