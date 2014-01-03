from flask import Flask
from flask.ext.zodb import ZODB

app = Flask(__name__)
app.config.from_object('config')
db = ZODB(app)

from app import views

