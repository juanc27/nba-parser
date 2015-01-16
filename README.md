nba-parser
==========

Python script to parse roster, schedule, stats and standings from nba.com and espn.go.com/nba. It uses python's BeautifulSoup4 html parser.

Requirements:
============
beautifulsoup4 (4.3.2)

Examples:
=========

from nba import getNBA_dot_com_Roster, getESPN_dot_com_Roster, getNBA_dot_com_PlayerStats
from nba import getNBA_dot_com_Standings, getNBA_dot_com_ScheduleCurrentTournament
from nba getNBA_dot_com_Schedule

results = getNBA_dot_com_Roster("Warriors")

--output--
### Warriors Roster - nba.com ###

first_name: Leandro  last_name: Barbosa  position: Guard  jersey_number: 19  image: http://stats.nba.com/media/players/230x185/2571.png  birthdate: 1982-11-28  height: 6.3  weight: 194  
first_name: Harrison  last_name: Barnes  position: Forward  jersey_number: 40  image: http://stats.nba.com/media/players/230x185/203084.png  birthdate: 1992-05-30  height: 6.8  weight: 225  
first_name: Andrew  last_name: Bogut  position: Center  jersey_number: 12  image: http://stats.nba.com/media/players/230x185/101106.png  birthdate: 1984-11-28  height: 7.0  weight: 260  

...
----------

results = getESPN_dot_com_Roster("Warriors")

--output--
### Warriors Roster - espn.com###

jersey_number: 19  first_name: Leandro  last_name: Barbosa  position: SG  age: 32  height: 6.3  weight: 194.0  college: None  salary: 915243  
jersey_number: 40  first_name: Harrison  last_name: Barnes  position: SF  age: 22  height: 6.8  weight: 225.0  college: North Carolina  salary: 3049920  
jersey_number: 12  first_name: Andrew  last_name: Bogut  position: C  age: 30  height: 7.0  weight: 260.0  college: Utah  salary: 12972973
...
----------

results = getNBA_dot_com_PlayerStats("Warriors")

--output--
### Warriors Player Stats - nba.com ###

first_name: Leandro  last_name: Barbosa  games_played: 20  field_goals_pct: 46.0  field_goals_3pt_pct: 16.0  free_throw_pct: 75.0  rebounds_per_game: 1.3  assists_per_game: 1.1  steals_per_game: 0.7  turnovers_per_game: 0.7  fouls_per_game: 1.6  points_per_game: 5.4  
first_name: Shaun  last_name: Livingston  games_played: 24  field_goals_pct: 51.0  field_goals_3pt_pct: 0  free_throw_pct: 77.0  rebounds_per_game: 2.1  assists_per_game: 2.8  steals_per_game: 0.8  turnovers_per_game: 1.5  fouls_per_game: 1.5  points_per_game: 5.9  
first_name: Andre  last_name: Iguodala  games_played: 24  field_goals_pct: 42.0  field_goals_3pt_pct: 31.0  free_throw_pct: 48.0  rebounds_per_game: 3.5  assists_per_game: 2.6  steals_per_game: 1.1  turnovers_per_game: 1.2  fouls_per_game: 1.2  points_per_game: 7.0 
...
----------

results = getNBA_dot_com_Schedule("Warriors")

--output--
### Warriors Schedule - nba.com ###
### Tournament : 2014-15 Regular Season ###

away_team: Thunder  away_city: Oklahoma City  home_team: Warriors  home_city: Golden State  away_score: 0  home_score: 0  stadium: ORACLE Arena  date: 2014-12-18T19:30:00-08:00  tournament: 2014-15 Regular Season  
away_team: Kings  away_city: Sacramento  home_team: Warriors  home_city: Golden State  away_score: 0  home_score: 0  stadium: ORACLE Arena  date: 2014-12-22T19:30:00-08:00  tournament: 2014-15 Regular Season  
away_team: Warriors  away_city: Golden State  home_team: Lakers  home_city: Los Angeles  away_score: 0  home_score: 0  stadium: Staples Center  date: 2014-12-23T19:30:00-08:00  tournament: 2014-15 Regular Season
...

---------

results = getNBA_dot_com_Standings()

--output--
### Standings - nba.com ###

conference: Eastern  division: Atlantic  name: Toronto  wins: 19  losses: 6  conference_wins: 12  conference_losses: 4  division_wins: 3  division_losses: 0  home_wins: 12  home_losses: 3  road_wins: 7  road_losses: 3  last10_wins: 6  last10_losses: 4  streak: W 3  
conference: Eastern  division: Atlantic  name: Brooklyn  wins: 10  losses: 13  conference_wins: 7  conference_losses: 8  division_wins: 4  division_losses: 1  home_wins: 5  home_losses: 7  road_wins: 5  road_losses: 6  last10_wins: 5  last10_losses: 5  streak: L 1  
conference: Eastern  division: Atlantic  name: Boston  wins: 8  losses: 14  conference_wins: 7  conference_losses: 7  division_wins: 3  division_losses: 2  home_wins: 5  home_losses: 8  road_wins: 3  road_losses: 6  last10_wins: 4  last10_losses: 6  streak: W 1
...
----------


