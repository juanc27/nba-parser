from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date, datetime
import re
from collections import OrderedDict

nba_url = "http://www.nba.com/"
espn_url = "http://espn.go.com/"

def print_dict(dict):
    print ""
    for field, value in dict.items():
        print "{}: {} ". format(field, value),

""" 
    returns a team's list of players and their info from on nba.com/<team_short_name>/roster/
    nba.com team names are like "warriors", "lakers", etc.
"""
def getNBA_dot_com_Roster(team_short_name = None):

    roster = list()
    if team_short_name == None:
        return
    url = nba_url + team_short_name.lower() + "/roster/"
    response = urlopen(url)
    try:
        data = response.read()
    except:
        print "**error visiting {}".format(url)
        raise
    soup = BeautifulSoup(data)
        
    players = soup.find_all(class_ = "roster__player")
    print "\n### {} Roster - nba.com ###\n".format(team_short_name)
    for player in players:
        resp = OrderedDict()
        name = player.find(class_ = "roster__player__header__heading")

        resp['first_name'] = name.string.split()[0]
        resp['last_name'] = name.string.split()[1]

        resp['position'] = player.find(class_ = "roster__player__header_position").string.split()[0]

        resp['jersey_number'] = int(player.find(class_ = "roster__player__header_jnumber").next)
        try:
            resp['image'] = player.find("img", class_ = "roster__player__bust").get("src")
        except:
            resp['image'] = None

        birthdate = player.find(class_="roster__player__info__bio__dob roster__player__info__bio--item").next.next.next
        resp['birthdate'] = datetime.strptime(birthdate, "%m/%d/%Y").date()
        height = player.find(class_="roster__player__info__bio__height roster__player__info__bio--item").next.next.next
        resp['height'] = float("{}.{}".format(height.split('\' ')[0], height.split('\' ')[1]))
        
        weight = player.find(class_="roster__player__info__bio__weight roster__player__info__bio--item").next.next.next
        resp['weight'] = int(weight[:3])

        print_dict(resp)
        
        roster.append(resp)
    
    return roster 

"""
    returns a value given a soup result from soup.find.
    type : "int", "float", "pct
"""
def get_value_or_0 (value, type):
    val = 0
    try:
        if type == 'pct':
            val = float(value.string[:2])
        elif type == 'int':
            val = int(value.string)
        elif type == 'float':
            val = float(value.string)
        else:
            raise
    except:
        val = 0
    return val

""" 
    same as get_value_or_0 but without .string
"""
def try_or_0 (value, type):
    val = 0
    try:
        if type == 'int':
            val = int(value)
        elif type == 'float':
            val = float(value)
        else:
            raise
    except:
        val = 0
    return val

""" 
    get soup from nba.com/standings/
"""
def getNBA_dot_com_Standings_soup():

    url = nba_url + "/standings/"
    response = urlopen(url)
    try:
        data = response.read()
    except:
        print "**error visiting {}".format(url)
        raise
    return BeautifulSoup(data)

""" 
    get CurrentTournament from nba.com/standings 
    adds "Regular Season" at the end to be consistent and different from Preseason
"""
def getNBA_dot_com_CurrentTournament():
    soup = getNBA_dot_com_Standings_soup()
    try:
        current_tournament = soup.find("title").string[10:19]
        #keep it in format YYYY-YY (ex. 1998-99)
        current_tournament = current_tournament[:5] + current_tournament[7:] + " Regular Season"
    except:
        current_tournament = None
    print "\n\nCurrent Tournament: {}".format(current_tournament)
    return current_tournament

""" 
    get soup from nba.com/<team>/stats/
"""
def getNBA_dot_com_PlayerStats_soup(team_short_name = None):

    if team_short_name == None:
        return None
    url = nba_url + team_short_name.lower() + "/stats/"
    response = urlopen(url)
    try:
        data = response.read()
    except:
        print "**error visiting {}".format(url)
        raise
    return BeautifulSoup(data)

"""
    get Current Tournament from nba.com/<team>/stats/ page
    this can be used for verification or to relate current tournament with stats
"""
def getNBA_dot_com_PlayerStatsCurrentTournament(team_short_name = None):
    soup = getNBA_dot_com_PlayerStats_soup(team_short_name)
    try: 
        current_tournament = soup.find(class_="pane-title").string[:7] + " Regular Season"
    except:
        current_tournament = None
    print "\n\nCurrent Tournament: {}".format(current_tournament)
    return current_tournament

"""
    returns a list of stats per player for a team from on nba.com/<team_short_name>/stats/
"""
def getNBA_dot_com_PlayerStats(team_short_name = None):

    stats = list()
    soup = getNBA_dot_com_PlayerStats_soup(team_short_name)

    players = soup.find("table", class_ = "stats-table player-stats season-averages hidden "\
                                          "table table-striped table-bordered sticky-enabled")

    print "\n\n### {} Player Stats - nba.com ###\n".format(team_short_name)
    players = players.find_all("tr")
    for player in players:

        if player.find("th"):
            continue
        
        resp = OrderedDict()
        name = player.find("a").text

        resp['first_name'] = name.split()[0]
        resp['last_name'] = name.split()[1]
        resp['games_played'] = get_value_or_0(player.find("td", class_="gp"), "int")
        resp['field_goals_pct'] = get_value_or_0(player.find("td", class_="fg_pct"), "pct")
        resp['field_goals_3pt_pct'] = get_value_or_0(player.find("td", class_="fg3_pct"), 
                                                        "pct")
        resp['free_throw_pct'] = get_value_or_0(player.find("td", class_="ft_pct"), "pct")
        resp['rebounds_per_game'] = get_value_or_0(player.find("td", class_="reb"), "float")
        resp['assists_per_game'] = get_value_or_0(player.find("td", class_="ast"), "float")
        resp['steals_per_game'] = get_value_or_0(player.find("td", class_="stl"), "float")
        resp['turnovers_per_game'] = get_value_or_0(player.find("td", class_="tov"), "float")
        resp['fouls_per_game'] = get_value_or_0(player.find("td", class_="pf"), "float")
        resp['points_per_game'] = get_value_or_0(player.find("td", class_="pts"), "float")
         
        print_dict(resp)
        stats.append(resp)
    return stats

"""
    get soup from nba.com/<team>/schedule/
"""
def getNBA_dot_com_Schedule_soup(team_short_name = None):

    if team_short_name == None:
        return None
    url = nba_url + team_short_name.lower() + "/schedule/"
    response = urlopen(url)
    try:
        data = response.read()
    except:
        print "**error visiting {}".format(url)
        raise
    return BeautifulSoup(data)

"""
    get Current Tournament from nba.com/<team>/schedule/ page
    this can be used for verification or to relate current tournament with schedule
"""
def getNBA_dot_com_ScheduleCurrentTournament(team_short_name = None):
    soup = getNBA_dot_com_Schedule_soup(team_short_name)
    try:
        current_tournament = soup.find("title").string[:7] + " Regular Season"
    except:
        current_tournament = None
    print "\n\nCurrent Tournament: {}".format(current_tournament)
    return current_tournament

"""
    returns a team's list of games per Tournament from on nba.com/<team_short_name>/schedule/
"""
def getNBA_dot_com_Schedule(team_short_name = None):

    stats = list()
    soup = getNBA_dot_com_Schedule_soup(team_short_name)

    print "\n\n### {} Schedule - nba.com ###\n".format(team_short_name)
    tournaments = soup.find_all("section", class_=re.compile("schedule"))
    for tournament in tournaments:
        name = tournament.find("h2", class_='schedule__header').text
        print "### Tournament : {} ###".format(name)

        games = tournament.find_all("li", class_ = "event")

        for game in games:

            resp = OrderedDict()
            try:
                resp['away_team'] = game.find("span",
                          class_="abbrv abbrv--visitor abbrv--team abbrv--visitor--team").text
                resp['away_city'] = game.find("span",
                        class_="city city--visitor city--team city--visitor--team").text
            except:
                resp['away_team'] = game.find("span",
                          class_="abbrv abbrv--visitor abbrv--opp abbrv--visitor--opp").text
                resp['away_city'] = game.find("span",
                        class_="city city--visitor city--opp city--visitor--opp").text

            try:
                resp['home_team'] = game.find("span",
                        class_="abbrv abbrv--home abbrv--team abbrv--home--team").text
                resp['home_city'] = game.find("span",
                        class_="city city--home city--team city--home--team").text
            except:
                resp['home_team'] = game.find("span",
                                    class_="abbrv abbrv--home abbrv--opp abbrv--home--opp").text
                resp['home_city'] = game.find("span",
                        class_="city city--home city--opp city--home--opp").text

            away_score = game.find("div", 
                                     class_='schedule__team-detail team-details--wins-losses')
            resp['away_score'] = get_value_or_0(away_score, "int")
            try:
                home_score = away_score.find_next("div",
                                    class_='schedule__team-detail team-details--wins-losses')
            except:
                home_score = None
            resp['home_score'] = get_value_or_0(home_score, "int")
            resp['stadium'] = game.attrs['data-arena']
            #to parse use dateutil.parser.parse(<date>) from python-dateutil
            #or parse_datetime(<date>) from django.utils.dateparse 
            resp['date'] = game.find("div", itemprop="startDate").attrs['content']
            resp['tournament'] = name

            print_dict(resp)
            stats.append(resp)
    return stats

"""
    returns nba standings from on nba.com/<team_short_name>/schedule/ by conference and division
"""
def getNBA_dot_com_Standings():

    standings = list()
    soup = getNBA_dot_com_Standings_soup()

    teams = soup.find("table", class_ = "genStatTable mainStandings")

    conference = None
    division = None
    print "\n\n### Standings - nba.com ###\n"
    teams = teams.find_all("tr")
    for team in teams:
   
        val = team.find("td", class_="confTitle")
        if val:
            conference = val.string.split()[0]
            continue

        val = team.find("td", class_="name") 
        if val: 
            division = val.string 
            continue

        team = team.find("td", class_="team")
        if team:
            resp = OrderedDict()
            resp['conference'] = conference
            resp['division'] = division
            pointer = team.find("a")
            resp['name'] = pointer.text
             
            pointer = pointer.find_next("td")
            resp['wins'] = get_value_or_0(pointer, "int")
            pointer = pointer.find_next("td")
            resp['losses'] = get_value_or_0(pointer, "int")
            pointer = pointer.find_next("td")

            #kinda ugly
            pointer = pointer.find_next("td")
            pointer = pointer.find_next("td") 

            resp['conference_wins'] = try_or_0(pointer.string.split("-")[0], "int")
            resp['conference_losses'] = try_or_0(pointer.string.split("-")[1], "int")

            pointer = pointer.find_next("td")
            resp['division_wins'] = try_or_0(pointer.string.split("-")[0], "int")
            resp['division_losses'] = try_or_0(pointer.string.split("-")[1], "int")
    
            pointer = pointer.find_next("td")
            resp['home_wins'] = try_or_0(pointer.string.split("-")[0], "int")
            resp['home_losses'] = try_or_0(pointer.string.split("-")[1], "int")

            pointer = pointer.find_next("td")
            resp['road_wins'] = try_or_0(pointer.string.split("-")[0], "int")
            resp['road_losses'] = try_or_0(pointer.string.split("-")[1], "int")

            pointer = pointer.find_next("td")
            resp['last10_wins'] = try_or_0(pointer.string.split("-")[0], "int")
            resp['last10_losses'] = try_or_0(pointer.string.split("-")[1], "int")

            pointer = pointer.find_next("td")
            resp['streak'] = pointer.text
            print_dict(resp)
            standings.append(resp)
    return standings


"""
    Converts nba.com team short names to espn style names 
    espn team names are like 'gs' for Golden State Warriors. 
"""
short_name_to_espn_name = {
'celtics' : 'bos',
'nets' : 'bkn',
'knick' : 'ny',
'76ers' : 'phi',
'raptors' : 'tor',
'bulls' : 'chi',
'cavaliers' : 'cle',
'pistons' : 'det',
'pacers' : 'ind',
'bucks' : 'mil',
'hawks' : 'atl',
'hornets' : 'cha',
'heat' : 'mia',
'magic' : 'orl',
'wizards' : 'wsh',
'warriors' : 'gs',
'clippers' : 'lac',
'lakers' : 'lal',
'suns' : 'phx',
'kings' : 'sac',
'mavericks' : 'dal',
'rockets' : 'hou',
'grizzlies' : 'mem',
'pelicans' : 'no',
'spurs' : 'sa',
'nuggets' : 'den',
'timberwolves' : 'min',
'thunder' : 'okc',
'blazers' : 'por',
'jazz' : 'utah',
}

"""
    returns a team's list of players and their info from 
    http://espn.go.com/nba/team/roster/_/name/<espn_team_short_name>/ 
    use team names are like "warriors", "lakers", etc.
"""                            
def getESPN_dot_com_Roster(team_short_name = None):

    roster = list()
    if team_short_name == None:
        return
    try:
        espn_team_name = short_name_to_espn_name[team_short_name.lower()]
    except:
        return None

    url = espn_url + "nba/team/roster/_/name/" + espn_team_name + "/"
    response = urlopen(url)
    try:
        data = response.read()
    except:
        print "**error visiting {}".format(url)
        raise
    soup = BeautifulSoup(data)
    
    players = soup.find_all("tr", class_ = re.compile("player"))
    print "\n\n### {} Roster - espn.com ###\n".format(team_short_name)
    for player in players:
        resp = OrderedDict()
        pointer = player.next.next
        resp['jersey_number'] = int(pointer)
        pointer = pointer.next.next.next
        name = pointer.string
        resp['first_name'] = name.string.split()[0]
        resp['last_name'] = name.string.split()[1]
        pointer = pointer.next.next
        resp['position'] = pointer.string
        pointer = pointer.next.next
        resp['age'] = int(pointer.string)
        pointer = pointer.next.next
        height = pointer.string
        resp['height'] = float("{}.{}".format(height.split("-")[0], height.split("-")[1]))
        pointer = pointer.next.next
        resp['weight'] = float(pointer.string)
        pointer = pointer.next.next
        college = pointer.string
        if college == u'\xa0':
            resp['college'] = None    
        else:
            resp['college'] = pointer.string
        
        pointer = pointer.next.next
        resp['salary'] = int(pointer.string.replace(",", "")[1:])

        print_dict(resp)

        roster.append(resp)
    return roster

if __name__ == "__main__":
    getNBA_dot_com_Roster("Warriors")
#    getESPN_dot_com_Roster("Warriors")
#    getNBA_dot_com_CurrentTournament()
#    getNBA_dot_com_PlayerStatsCurrentTournament("Warriors")
#    getNBA_dot_com_PlayerStats("Warriors")
#    getNBA_dot_com_Standings()
#    getNBA_dot_com_ScheduleCurrentTournament("Warriors")
#    getNBA_dot_com_Schedule("Warriors")
