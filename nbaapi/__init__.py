import os, sys, json
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
DEV_DATABASE_URL = 'postgresql://foobar:foobar@localhost/nba_api'
uri = os.environ.get('DATABASE_URL', DEV_DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['DEBUG'] = True
db = SQLAlchemy(app)

import nbaapi.views