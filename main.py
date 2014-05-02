import os, sys, json
# from models import *
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy import *
from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# Session = sessionmaker()
# db = create_engine("sqlite:///shots.db", 
#                     connect_args={'check_same_thread':False})
# Session.configure(bind=db)
# session = Session()

@app.route('/')
def index():
    return "Foo"

# @app.route('/teams', defaults={'team_id': None}, methods=['GET'], strict_slashes=False)    
# @app.route('/teams/<int:team_id>', methods=['GET'], strict_slashes=False)
# def teams(team_id):
#     if team_id: teams = session.query(Team).filter_by(id=team_id)    
#     else: teams = session.query(Team).all()
#     d = {'teams': []}
#     for t in teams:
#         team_vals = {'id': t.id, 'name': t.name, 'players': []}
#         for p in t.players:
#             team_vals['players'].append({'id': p.id, 'full_name': p.full_name})
#         d['teams'].append(team_vals)
#     return json.dumps(d)

# @app.route('/players', methods=['GET'], strict_slashes=False, defaults={'player_id': None})
# @app.route('/players/<int:player_id>', methods=['GET'], strict_slashes=False)
# def players(player_id):
#     if player_id: players = session.query(Player).filter_by(id=player_id)
#     else: players = session.query(Player).all()
#     ps = {'players': []}
#     for p in players:
#         ps.append({
#             'full_name': p.full_name, 
#             'id': p.id, 
#             'n_shots': p.n_shots,
#             'team_id': p.team_id
#         })
#     return json.dumps(ps)

# @app.route('/get_shot_data', methods=['GET'])
# def get_shot_data():
#     """
#     Returns shot totals as json list. 
#     """
#     testing = True
#     player_id = request.args.get('player_id')
#     q =  "select xcoord, ycoord, shotresult, " + \
#         " shot_type from shots where player_id=" + player_id 
#     sqlresponse = session.execute(q)
#     shot_rows = [list(row) for row in sqlresponse.fetchall()]
#     filtered_shot_rows = free_throw_filter(shot_rows)
#     hm = Heatmap(filtered_shot_rows)
#     print hm.get_json_data()
#     return json.dumps(hm.get_json_data())
if __name__ == "__main__":
    app.run(debug=True)