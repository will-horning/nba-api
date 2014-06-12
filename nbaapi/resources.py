from nbaapi import app, db, mongo
from models import Shot, Team, Game, Player
from nbaapi import app, db, mongo, api
from flask.ext.restful import reqparse
from flask.ext import restful


class TeamAPI(restful.Resource):
	def get(self, id):
		return Team.query.filter_by(id=id).first().to_dict()


class GameAPI(restful.Resource):
	def get(self, id):
		return Game.query.filter_by(id=id).first().to_dict()


class PlayerAPI(restful.Resource):
	def get(self, id):
		return Player.query.filter_by(id=id).first().to_dict()


class ModelListAPI(restful.Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('page', type=int, required=False)
		self.reqparse.add_argument('per_page', type=int, required=False)
		self.reqparse.add_argument('fields', type=str, required=False)
		for name, t in self.exposed_fields.iteritems():
			self.reqparse.add_argument(name, type=t, required=False)
		super(ModelListAPI, self).__init__()

	def get(self):
		args = {k: v for k, v in self.reqparse.parse_args().iteritems() if v}
		model_args = {}
		for k, v in args.iteritems():
			if k in self.exposed_fields.keys(): model_args[k] = v
		results = []
		for m in self.model.query.filter_by(**model_args):
			results.append(m.to_dict())
		if 'page' in args:
			page = args['page']
			per_page = args.get('per_page', 10)
			results = results[page * per_page:(page + 1) * per_page]
		if 'fields' in args:
			fields = args['fields'].split(',')
			for row in results:
				for k in row.keys():
					if k not in fields: del row[k]
		return {'teams': results}


class TeamsAPI(ModelListAPI):
	model = Team
	exposed_fields =  {'id': int, 'name': str, 'season': str}

class PlayersAPI(ModelListAPI):
	model = Player
	exposed_fields = {'id': int, 
		'fullname': str, 'team_id': int, 'n_shots': int}

class GamesAPI(ModelListAPI):
	model = Game
	exposed_fields = {'home_team_id': int, 'away_team_id': int}


class ShotsAPI(restful.Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('player_id', type=int, required=False)
		self.reqparse.add_argument('page', type=int, required=False)
		self.reqparse.add_argument('per_page', type=int, required=False)
		self.reqparse.add_argument('fields', type=str, required=False)

	def get(self):
		args = {k: v for k, v in self.reqparse.parse_args().iteritems() if v}
		player_id = args.get('player_id', None)
		filter_args = {'player_id': player_id} if player_id else {}
		results = list(mongo.shots.find(filter_args, {'_id': False}))
		if 'page' in args:
			page = args['page']
			per_page = args.get('per_page', 10)
			results = results[page * per_page:(page + 1) * per_page]
		if 'fields' in args:
			fields = args['fields'].split(',')
			for row in results:
				for k in row.keys():
					if k not in fields: del row[k]

		for row in results:
			del row['datetime']
		return {'shots': results}

api.add_resource(ShotsAPI, '/api/v1.0/shots')
api.add_resource(TeamsAPI, '/api/v1.0/teams')
api.add_resource(PlayersAPI, '/api/v1.0/players')
api.add_resource(GamesAPI, '/api/v1.0/games')
api.add_resource(TeamAPI, '/api/v1.0/team/<int:id>')
api.add_resource(TeamAPI, '/api/v1.0/player/<int:id>')
api.add_resource(TeamAPI, '/api/v1.0/game/<int:id>')