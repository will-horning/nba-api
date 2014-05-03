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
else:
    mongo_conn = pymongo.Connection('localhost', 27017)
mongo = mongo_conn['shots_db']


# from nbaapi.models import Shot, Player
# i = len(db.session.query(Player).all())
# with app.app_context():
#     for p in db.session.query(Player).all():
#         print i
#         print p.full_name
#         for s in p.shots:
#             fields = s.__dict__.copy()
#             del fields['_sa_instance_state']
#             mdb.shots.insert(fields)
#         i -= 1

import nbaapi.views