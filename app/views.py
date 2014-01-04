from app import app, db
from flask import render_template, request, flash, jsonify, url_for
from datetime import datetime
from pytz import timezone
from models import FillUp
import os, csv
from time import strptime
from decimal import Decimal

@app.route('/')
def index():
    return render_template("index.html")

def getFillUpsTree():
    if not db.has_key("fillUps"):
        from BTrees.OOBTree import OOBTree
        db["fillUps"] = OOBTree()

    return db["fillUps"]
    
@app.route('/submitMileage', methods = ['POST'])
def submitMileage():
    tree = getFillUpsTree()
    fillUp = FillUp(datetime.utcnow(), request.form["miles"], 
        request.form["price"], request.form["gallons"], request.form["latitude"],
        request.form["longitude"])
    tree[fillUp.date] = fillUp

    flash("Fillup Saved")
    flash("Fillup Cost: {0}".format(fillUp.price * fillUp.gallons))
    flash("Mileage: {0}".format(fillUp.miles * fillUp.price))

@app.route('/recentHistory')
def recentHistory():
    tree = getFillUpsTree()
    print("Record Count: {0}".format(len(tree)))
    recentHistory = []
    for index, value in tree.iteritems():
        print("key,value: {0},{1}".format(index, value))
        recentHistory.append(value)
        if len(recentHistory) >= 5:
            break

    return render_template("recentHistory.html", recentHistory = recentHistory)

@app.route('/import')
def importRecords():
    records = []
    csvImportFile = app.config['MILEAGE_IMPORT_CSV']

    with open(csvImportFile) as f:
        data = csv.reader(f)
        fields = data.next()

        fillUpTree = getFillUpsTree()

        for row in data:
            if len(row) == 0:
                break
            items = zip(fields, row)
            item = {}
            for (name, value) in items:
                item[name] = value
            fillUp = FillUp(
                date = convertToUtcDate(strptime(item["Date"], "%Y-%m-%d %H:%M:%S"))
                , miles = Decimal(item["FillUpMileage"])
                , gallons = Decimal(item["FillUpGallons"])
                , price = Decimal(item["FillUpCostPerGallon"])
                , latitude = Decimal(item["Latitude"])
                , longitude = Decimal(item["Longitude"]))

            print("Date: {0}".format(fillUp.date))
            fillUpTree[fillUp.date] = fillUp
            records.append(fillUp)

    return render_template("import_results.html", records = records)

def convertToUtcDate(time_struct):
    estzone = timezone("US/Eastern")
    utczone = timezone("UTC")
    if time_struct.tm_hour == 0 and time_struct.tm_min == 0 and time_struct.tm_sec == 0:
        estDateTime = datetime(year = time_struct.tm_year, 
            month = time_struct.tm_mon, 
            day = time_struct.tm_mday, 
            tzinfo = estzone)
    else:
        estDateTime = datetime(year = time_struct.tm_year, 
            month = time_struct.tm_mon, 
            day = time_struct.tm_mday, 
            hour =  time_struct.tm_hour,
            minute = time_struct.tm_min,
            second = time_struct.tm_sec,
            tzinfo = estzone)

    utcDateTime = estDateTime.astimezone(utczone)
    return utcDateTime 

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)

    return url_for(endpoint, **values)
