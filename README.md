API for NBA data scraped from CBSSports.com. Live version [here](http://nba-api.herokuapp.com). 

Right now it only contains data for the 2013-2014 season, I'll update it to include past seasons soon.

This is a very early work in progess, only a few featuers are supported thus far.

#Usage

Only GET requests are supported. All requests support pagination using the following arguments:
page: The page number.
per_page: The number of objects per page.
Example:
```
/teams/?page=2&?per_page=10
```

####Teams
```
/teams/
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

```
/teams/<int:team_id>
```
Returns the team with the given team_id.

```
/teams/<team_name>
```
Returns all teams with the given name (City, followed by team name, e.g. Chicago Bulls.) Right now the db only contains the 2013-2014 season. Eventually I'll include previous seasons where the same team from different seasons are considered distinct team objects (so the 2013 Bulls would be a seperate object from the 2012 Bulls).

####Players

```
/players/
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

```
/players/<int:player_id>
```

Returns the player with the listed id number.

####Shots

```
/shots/
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

```
/shots/<int:player_id>
```
Returns all shots taken by the player with the given id.

####Games
```
/games/
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