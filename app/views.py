from app import app, db
from flask import render_template, request, flash, jsonify, url_for, redirect
from datetime import datetime, timedelta
from pytz import timezone
from models import FillUp
import os, csv
from time import strptime
from decimal import Decimal
from forms import EditMileageForm, MileageForm

@app.route('/')
def index():
    form = MileageForm()
    return render_template("index.html", form = form, url = "/")

def getFillUpsTree():
    if not db.has_key("fillUps"):
        from BTrees.OOBTree import OOBTree
        db["fillUps"] = OOBTree()

    return db["fillUps"]
    
@app.route('/submitMileage', methods = ['POST'])
def submitMileage():
    tree = getFillUpsTree()
    utczone = timezone("UTC")
    latitude = request.form["latitude"]
    if not latitude:
        latitude = 0
    longitude = request.form["longitude"]
    if not longitude:
        longitude = 0
    dateKey = datetime.now(utczone).replace(microsecond=0)
    fillUp = FillUp(dateKey, Decimal(request.form["miles"]), 
        Decimal(request.form["price"]), 
        Decimal(request.form["gallons"]), 
        Decimal(latitude),
        Decimal(longitude))
    tree[fillUp.date] = fillUp

    flash("Fillup Saved")
    flash("Fillup Cost: {0}".format(fillUp.price * fillUp.gallons))
    flash("Mileage: {0}".format(fillUp.mileage))
    response = {}
    response["success"] = True
    return jsonify(response)

@app.route('/edit/<date>', methods = ["POST", "GET"])
def editDate(date):
    dt = getUTCDateFromString(date)
    form = EditMileageForm()
    fillUpRecord = getFillUpsTree()[dt]
    template = None
    if request.method == 'GET':
        form.miles.data = fillUpRecord.miles
        form.price.data = fillUpRecord.price
        form.gallons.data = fillUpRecord.gallons
        template = render_template("editRecord.html", record = fillUpRecord, form = form, dateKey = date)
    else: 
        fillUpRecord.miles = Decimal(form.miles.data)
        fillUpRecord.price = Decimal(form.price.data)
        fillUpRecord.gallons = Decimal(form.gallons.data)
        template = redirect(url_for("history"))
    return template

@app.route('/recentHistory')
def recentHistory():
    tree = getFillUpsTree()
    recentHistory = []
    if len(tree) > 0:
        key = tree.maxKey()
        while len(recentHistory) < 5:
            recentHistory.append(tree[key])
            oneSecondEarlier = key + timedelta(seconds = -1)
            key = tree.maxKey(oneSecondEarlier)

    return render_template("recentHistory.html", recentHistory = recentHistory)

@app.route('/history')
def history():
    tree = getFillUpsTree()
    recentHistory = []
    maxKey = tree.maxKey()
    minKey = tree.minKey()
    while maxKey > minKey:
        recentHistory.append(tree[maxKey])
        oneSecondEarlier = maxKey + timedelta(seconds = -1)
        maxKey = tree.maxKey(oneSecondEarlier)

    return render_template("full_history.html", recentHistory = recentHistory, url = "history")

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

            fillUpTree[fillUp.date] = fillUp
            records.append(fillUp)

    return render_template("import_results.html", records = records)

@app.route('/migrate')
def migrate():
    tree = getFillUpsTree()

    for fuKey in tree:
        if fuKey.microsecond > 0:
            fuObj = tree[fuKey]
            del tree[fuObj.date]
            fuObj.date = fuObj.date.replace(microsecond = 0)
            print(fuObj)
            tree[fuObj.date] = fuObj
    return "Migration Complete"

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

def getUTCDateFromString(dateString):
    time_struct = strptime(dateString, "%Y_%m_%d_%H_%M_%S")
    utcDateTime = datetime(year = time_struct.tm_year, 
            month = time_struct.tm_mon, 
            day = time_struct.tm_mday, 
            hour =  time_struct.tm_hour,
            minute = time_struct.tm_min,
            second = time_struct.tm_sec,
            tzinfo = timezone("UTC"))
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
