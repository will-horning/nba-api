import os, sys
from flask import Flask, request, render_template, make_response, jsonify
from nbaapi import app, db, mongo
from models import Shot, Team, Game, Player
from bson import json_util
from time import strftime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/')
def index():
    return jsonify({'api': 'nba_api', 'version': '1.0'})

@app.route('/teams', defaults={'team_id': None}, methods=['GET'], 
    strict_slashes=False)    
@app.route('/teams/<int:team_id>', methods=['GET'], strict_slashes=False)
def teams(team_id):
    if team_id: teams = db.session.query(Team).filter_by(id=team_id)    
    else: teams = db.session.query(Team).filter_by(**db_filters(request)).all()
    d = {'teams': []}
    for t in teams:
        team_vals = t.to_dict()
        team_vals['players'] = [p.to_dict() for p in t.players]
        d['teams'].append(team_vals)
    return jsonify(d)

@app.route('/players', methods=['GET'], defaults={'player_id': None}, 
    strict_slashes=False)
@app.route('/players/<int:player_id>', methods=['GET'], strict_slashes=False)
def players(player_id):
    if player_id: 
        players = db.session.query(Player).filter_by(id=player_id).all()
    else: 
        filters = db_filters(request)
        if 'team' in filters: del filters['team']
        if filters:
            players = db.session.query(Player).filter_by(**filters).all()
        else:
            players = db.session.query(Player).all()
        if 'team' in request.args:
            players = [p for p in players if p.team.name == request.args['team']]
    return jsonify({'players': [p.to_dict() for p in players]})

@app.route('/shots/<int:player_id>', methods=['GET'], strict_slashes=False)
@app.route('/shots', methods=['GET'], defaults={'player_id': None}, 
    strict_slashes=False)
def shots(player_id):
    shots = []
    filters = {'player_id': player_id} if player_id else db_filters(request)
    for shot in mongo.shots.find(filters):
        del shot['_id']
        shot['datetime'] = shot['datetime'].strftime(DATE_FORMAT)
        shots.append(shot)
    return jsonify({'shots': shots})

def db_filters(r):
    filters = dict(r.args.items())
    for k, v in filters.iteritems():
        if 'id' in k: filters[k] = int(v)
    return filters