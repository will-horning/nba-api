from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
import datetime, json

db = create_engine("postgresql+psycopg2://will:getusome@localhost/nba_api")
Base = declarative_base()

QUARTER_LENGTH_IN_MIN = 12 # Used for converting game time to absolute time.

# Shot types are recorded in CBS Sports data as an integer corresponding to these values:
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


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    season = Column(String)
    players = relationship("Player", backref="team")
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Game(Base):
	__tablename__ = "games"
	id = Column(Integer, primary_key=True)
	home_team_id = Column(Integer, ForeignKey("teams.id"))
	away_team_id = Column(Integer, ForeignKey("teams.id"))
	datetime = Column(DateTime)
	shots = relationship("Shot", backref="game")
	away_team = relationship("Team", foreign_keys=away_team_id)
	home_team = relationship("Team", foreign_keys=home_team_id)
	series_n = Column(Integer)

	def __init__(self, home_team, away_team, game_datetime, series_n):
		self.home_team = home_team
		self.away_team = away_team
		self.datetime = game_datetime
		self.series_n = series_n

class Player(Base):
	__tablename__ = "players"

	id = Column(Integer, primary_key=True)
	full_name = Column(String)
	team_id = Column(Integer, ForeignKey("teams.id"))
	n_shots = Column(Integer)
	shots = relationship("Shot", backref="player")

	def __init__(self, pid, full_name, team):
		self.id = pid
		self.full_name = full_name
		self.team = team

	def __repr__(self):
		return self.full_name + " " + str(self.id)

class Shot(Base):
	__tablename__ = "shots"
	id = Column(Integer, primary_key=True)
	shotresult = Column(Integer)
	datetime = Column(DateTime)
	quarter = Column(Integer)
	player_id = Column(Integer, ForeignKey('players.id'))
	game_id = Column(Integer, ForeignKey('games.id'))
	shot_type = Column(String(50))
	xcoord = Column(Integer)
	ycoord = Column(Integer)
	distance = Column(Integer)
	homeaway = Column(String(4))
	
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
		This function converts the game time string to a datetime instance recording the exact time and
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
		

Base.metadata.create_all(db)
