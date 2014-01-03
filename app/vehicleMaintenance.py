#!/usr/local/bin/python

import datetime
import cgi;
import cgitb; cgitb.enable()  # for troubleshooting
import math;
import MileageDbInput
from mileage.models import *

print "Content-Type: text/html" # HTML is following
print # blank line, end of headers


fields = cgi.FieldStorage()
pageNum, pageSize = 1, 25
if "page" in fields and "pageSize" in fields:
	pageNum = int(fields["page"].value)
	pageSize = int(fields["pageSize"].value)

totalRows = Vehiclemaintenance.objects.all().count()
pages = math.ceil(float(totalRows) / float(pageSize))
rangeStart = 1
if pageNum > pages / 2:
	rangeStart = pageNum - 5

pagesToShow = 5
pagingHtml = ""

if pageNum > 1:
	pagingHtml += """<a href="vehicleMaintenance.py?page=%s&pageSize=%s"><- Prev</a>&nbsp;&nbsp;""" \
		 % (pageNum - 1, pageSize)

count = 1
for i in range(rangeStart, pages):
	page = i + 1
	pagingHtml += "<a href='vehicleMaintenance.py?page=%s&pageSize=%s'>%s</a>&nbsp;" % (page, pageSize, page)
	if count > 5:
		break;
	else:
		count += 1

if pageNum < pages:
	pagingHtml += """<a href="vehicleMaintenance.py?page=%s&pageSize=%s">Next -></a>""" % (pageNum + 1, pageSize)

print """<html>
	<head><style>
		a {
			-webkit-text-size-adjust: 150%%;
		}
	</style>
	</head><body>
	<meta name="viewport" content="width=340, initial-scale=1.0, user-scalable=no"/>
	<a href="fillupinput.py"><- Back</a>
	<p></p>
	<b>Page:</b> %s
	<b>Page Select</b>: <p>%s</p>
	<p></p>
	<table cellpadding="4" cellspacing="0" border="1">
	<tr><th>Date</th>
		<th>Miles</th><th>Gallons</th><th>Cost</th><th>Mileage</th>
	</tr>
""" % (pageNum, pagingHtml) 

results = MileageDbInput.GetVehicleMaintenance(pageNum, pageSize)
for row in results:
	print "<tr>"
	print "<td><label title='%s'>%s</label></td>" % (row.date,
		row.date.strftime("%m/%d/%Y"))
	mileage = round(row.fillupmileage / row.fillupgallons, 2)
	print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
		% (round(row.fillupmileage, 1), row.fillupgallons, round(row.fillupcostpergallon, 2), mileage)
	print "</tr>"

print """
	</table>
	<p></p>
	<b>Page Select:</a> <p>%s</p>
""" % (pagingHtml)

print "</body></html>"
