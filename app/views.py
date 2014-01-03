from app import app, db
from flask import render_template, request, flash, jsonify, url_for
from datetime import datetime
from models import FillUp
import os

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
    fillUp = FillUp(datetime.now(), request.form["miles"], 
        request.form["price"], request.form["gallons"], request.form["latitude"],
        request.form["longitude"])
    tree[fillUp.date] = fillUp

    flash("Fillup Saved")
    result = {}
    result["success"] = True
    result["message"] = ""
    return jsonify(result)

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

        
