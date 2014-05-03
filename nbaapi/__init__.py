import os, sys, json, pymongo
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.pymongo import PyMongo 


app = Flask(__name__)
DEV_DATABASE_URL = 'postgresql://foobar:foobar@localhost/nba_api'
uri = os.environ.get('DATABASE_URL', DEV_DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['DEBUG'] = True
db = SQLAlchemy(app)

mongo_url = os.environ.get('MONGOHQ_URL')
if mongo_url:
    mongo_conn = pymongo.Connection(mongo_url)
    mongo = mongo_conn.nba_api_shots
else:
    mongo_conn = pymongo.Connection('localhost', 27017)
    mongo = mongo_conn['shots_db']

import nbaapi.views