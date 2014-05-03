import os, sys, json
from flask import Flask, request, render_template
from nbaapi import app, db
from models import Shot, Team, Game, Player


@app.route('/')
def index():
    return 'Foo'

@app.route('/teams', defaults={'team_id': None}, methods=['GET'], strict_slashes=False)    
@app.route('/teams/<int:team_id>', methods=['GET'], strict_slashes=False)
def teams(team_id):
    if team_id: teams = db.session.query(Team).filter_by(id=team_id)    
    else: teams = db.session.query(Team).all()
    d = {'teams': []}
    for t in teams:
        team_vals = {'id': t.id, 'name': t.name, 'players': []}
        for p in t.players:
            team_vals['players'].append({'id': p.id, 'full_name': p.full_name})
        d['teams'].append(team_vals)
    return json.dumps(d)

@app.route('/players', methods=['GET'], strict_slashes=False, defaults={'player_id': None})
@app.route('/players/<int:player_id>', methods=['GET'], strict_slashes=False)
def players(player_id):
    if player_id: players = db.session.query(Player).filter_by(id=player_id)
    else: players = db.session.query(Player).all()
    ps = {'players': []}
    for p in players:
        ps['players'].append({
            'full_name': p.full_name, 
            'id': p.id, 
            'n_shots': p.n_shots,
            'team_id': p.team_id
        })
    return json.dumps(ps)
