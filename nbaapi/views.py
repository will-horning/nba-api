from flask import Flask, request, make_response, jsonify
from nbaapi import app, db, mongo
from models import Shot, Team, Game, Player
from time import strftime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_PAGE_LENGTH = 10

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/')
def index():
    return jsonify({'api': 'nba_api', 'version': '1.0'})

@app.route('/teams', methods=['GET'], strict_slashes=False)    
def all_teams():
    response = {'teams': [t.to_dict() for t in Team.query.all()]}
    return jsonify(paginate('teams', response, request))


@app.route('/teams/<int:team_id>', methods=['GET'], strict_slashes=False)
def team_by_id(team_id):
    t = Team.query.filter_by(id=team_id).first()
    return jsonify(paginate('teams', {'teams': [t.to_dict()]}, request))


@app.route('/teams/<name>', methods=['GET'], strict_slashes=False)
def teams_by_name(name):
    teams = Team.query.filter_by(name=name).all()
    response = {'teams': [t.to_dict() for t in teams]}
    return jsonify(paginate('teams', response, request))


@app.route('/teams/<name>/<season>', methods=['GET'], strict_slashes=False)
def team_by_name_season(name, season):
    t = Team.query.filter_by(name=name, season=season).first()
    return jsonify(paginate('teams', {'teams': [t.to_dict()]}, request))


@app.route('/players', methods=['GET'], strict_slashes=False)
def all_players():
    players = Player.query.all()
    response = {'players': [p.to_dict() for p in players]}
    return jsonify(paginate('players', response, request))


@app.route('/players/<int:player_id>', methods=['GET'], strict_slashes=False)
def player_by_id(player_id):
    p = Player.query.filter_by(id=player_id).first()
    return jsonify(paginate('players', {'players': [p.to_dict()]}, request))


@app.route('/shots', methods=['GET'], strict_slashes=False)
def all_shots():
    shots = list(mongo.shots.find({}, {'_id': False}))
    return jsonify(paginate('shots', {'shots': shots}, request))

@app.route('/shots/<int:player_id>', methods=['GET'], strict_slashes=False)
def shots_by_player_id(player_id):
    shots = list(mongo.shots.find({'player_id': player_id}, {'_id': False}))
    return jsonify(paginate('shots', {'shots': shots}, request))

@app.route('/games/', methods=['GET'], strict_slashes=False)
def all_games():
    response = {'games': [g.to_dict() for g in Game.query.all()]}
    return jsonify(paginate('games', response, request))

def paginate(key, results, request):
    if 'page' not in request.args: return results
    n_page = int(request.args['page'])
    per_page = int(request.args.get('per_page', DEFAULT_PAGE_LENGTH))
    start = n_page * per_page
    end = min(len(results[key]), start + per_page)
    if start >= len(results[key]): return {'error': 'page number exceeds results size'}
    results[key] = results[key][start:end]
    return results