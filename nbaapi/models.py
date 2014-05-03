import datetime, json
from nbaapi import db

QUARTER_LENGTH_IN_MIN = 12 # Used for converting game time to absolute time.

# Shot types are recorded in CBS Sports data as an db.Integer corresponding to these values:
shot_type_map = {}
shot_type_map[0] = "Shot"
shot_type_map[1] = "Jump Shot"
shot_type_map[2] = "Running Jump"
shot_type_map[3] = "Hook Shot"
shot_type_map[4] = "Tip-in"
shot_type_map[5] = "Layup"
shot_type_map[6] = "Driving Layup"
shot_type_map[7] = "Dunk Shot"
shot_type_map[8] = "Slam Dunk"
shot_type_map[9] = "Driving Dunk"
shot_type_map[10] = "Free Throw"
shot_type_map[11] = "1st of 2 Free Throws"
shot_type_map[12] = "2nd of 2 Free Throws"
shot_type_map[13] = "1st of 3 Free Throws"
shot_type_map[14] = "2nd of 3 Free Throws"
shot_type_map[15] = "3rd of 3 Free Throws"
shot_type_map[16] = "Technical Free Throw"
shot_type_map[17] = "1st of 2 Free Throws"
shot_type_map[18] = "2nd of 2 Free Throws"
shot_type_map[19] = "Finger Roll"
shot_type_map[20] = "Reverse Layup"
shot_type_map[21] = "Turnaround Jump Shot"
shot_type_map[22] = "Fadeaway Jump Shot"
shot_type_map[23] = "Floating Jump Shot"
shot_type_map[24] = "Leaning Jump Shot"
shot_type_map[25] = "Mini Hook Shot"


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    season = db.Column(db.String)
    players = db.relationship("Player", backref="team")
    
    def __init__(self, name, season):
    	self.season = season
        self.name = name

    def __repr__(self):
        return self.name

class Game(db.Model):
	__tablename__ = "games"
	id = db.Column(db.Integer, primary_key=True)
	home_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
	away_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
	datetime = db.Column(db.DateTime)
	shots = db.relationship("Shot", backref="game")
	away_team = db.relationship("Team", foreign_keys=away_team_id)
	home_team = db.relationship("Team", foreign_keys=home_team_id)
	series_n = db.Column(db.Integer)

	def __init__(self, home_team, away_team, game_datetime, series_n):
		self.home_team = home_team
		self.away_team = away_team
		self.datetime = game_datetime
		self.series_n = series_n

class Player(db.Model):
	__tablename__ = "players"

	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String)
	team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
	n_shots = db.Column(db.Integer)
	shots = db.relationship("Shot", backref="player")

	def __init__(self, pid, full_name, team):
		self.id = pid
		self.full_name = full_name
		self.team = team

	def __repr__(self):
		return self.full_name + " " + str(self.id)

class Shot(db.Model):
	__tablename__ = "shots"
	id = db.Column(db.Integer, primary_key=True)
	shotresult = db.Column(db.Integer)
	datetime = db.Column(db.DateTime)
	quarter = db.Column(db.Integer)
	player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
	shot_type = db.Column(db.String(50))
	xcoord = db.Column(db.Integer)
	ycoord = db.Column(db.Integer)
	distance = db.Column(db.Integer)
	homeaway = db.Column(db.String(4))
	
	def __repr__(self):
		ret = []
		if self.shotresult: ret = ["Made"]
		else: ret = ["Missed"]
		ret += [" shot by ", self.player.firstname + " " + self.player.lastname]
		return "".join(ret)

	def __init__(self, shot_data_string, date_string, game, player):
		shot_data = shot_data_string.split(",")
		self.shotresult = int(shot_data[0])
		self.quarter = int(shot_data[2])
		self.datetime = self.get_absolute_time(shot_data[1], date_string)
		self.shot_type = shot_type_map[int(shot_data[5])]
		self.xcoord = int(shot_data[6])
		self.ycoord = int(shot_data[7])
		self.distance = int(shot_data[8].replace('"', ''))
		self.game = game
		self.player = player

	def get_absolute_time(self, game_time_string, date_string):
		"""
		CBS Sports data records the time for a shot as the time remaining in the current quarter.
		This function converts the game time db.String to a datetime instance recording the exact time and
		date the shot was taken (for now the hour field is left to zero).
		"""
		minutes_remaining = 0
		seconds_remaining = 0
		if ":" in game_time_string:
			minutes_remaining = int(game_time_string.split(":")[0])
			seconds_remaining = int(game_time_string.split(":")[1])
		elif "." in game_time_string:
			seconds_remaining = int(game_time_string.split(".")[0])
		dt = datetime.datetime(int(date_string[:4]), int(date_string[4:6]),
									   int(date_string[6:8]), 0, 0, 0)
		dt += datetime.timedelta(minutes = QUARTER_LENGTH_IN_MIN * self.quarter)
		dt -= datetime.timedelta(minutes = minutes_remaining, seconds = seconds_remaining)
		return dt
		
