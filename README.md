API for NBA data scraped from CBSSports.com. Live version [here](http://nba-api.herokuapp.com). 

Right now it only contains data for the 2013-2014 season, I'll update it to include past seasons soon.

This is a very early work in progess, only a few featuers are supported thus far.

[foo](nba-api/models.py)

#Usage

Only GET requests are supported. All requests support pagination using the following arguments:
page: The page number.
per_page: The number of objects per page.
Example:
```
/teams?page=2&per_page=10
```

#Base url:
```
http://nba-api.herokuapp.com/api/v1.0
```

####Teams
```
/teams
```
Retrives all teams.

Example:
```Javascript
{
  "id": 3, 
  "name": "Orlando Magic", 
  "players": [
    {
      "full_name": "Andrew Nicholson", 
      "id": 1992818, 
      "n_shots": null, 
      "team": "Orlando Magic", 
      "team_id": 3
    } 
    // All players on this team listed.
  ], 
  "season": "2013"
}
```

Filter options: name, id, season
```
/api/v1.0/teams?name=Orlando+Magic&season=2014&id=10
```

```
/team/<int:team_id>
```
Returns the team with the given team_id.

####Players

```
/players
```
Returns all players in the league.

Example:
```Javascript
{
  "full_name": "Rashard Lewis", 
  "id": 20613, 
  "n_shots": 1045, 
  "team": "Miami Heat", 
  "team_id": 6
}
 
```

Filter options: fullname, team_id, id
```
/api/v1.0/players?fullname=Kobe+Bryant&team_id=10&id=103334
```


```
/player/<int:player_id>
```

Returns the player with the listed id number.

####Shots

```
/shots
```
Returns every shot taken in every season by every player.

Example:
```Javscript
{
  "datetime": "Tue, 29 Oct 2013 00:02:24 GMT", 
  "distance": 0, 
  "game_id": 1, 
  "homeaway": 0, 
  "id": 13, 
  "player_id": 1622538, 
  "quarter": 1, 
  "shot_type": "Shot", 
  "shotresult": 1, 
  "xcoord": 0, 
  "ycoord": -42
}
```

Filter by: player_id
```
/api/v1.0/shots?player_id=103223
```

####Games
```
/games
```
Returns all games over every season.

Example:
```Javascript
{
  "away_team": "Orlando Magic", 
  "away_team_id": 3, 
  "datetime": "Tue, 29 Oct 2013 00:00:00 GMT", 
  "home_team": "Indiana Pacers", 
  "home_team_id": 4, 
  "id": 1, 
  "series_n": 0
}
```
