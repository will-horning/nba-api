import os, sys, json
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
DEV_DATABASE_URL = 'postgresql://foobar:foobar@localhost/nba_api'
uri = os.environ.get('DATABASE_URL', DEV_DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from nbaapi.models import Shot, Player
ps = db.session.query(Player).all()
d = {}
for p in ps:
    ss = []
    for s in p.shots:
        fields = s.__dict__.copy()
        del fields['_sa_instance_state']
        del fields['datetime']
        ss.append(fields)
    d[p.full_name] = ss
f = open('foo.json', 'w')
json.dump(d, f)
f.close()

import nbaapi.views