from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
PLAYER_KEYS = {'turnovers', 'attempted_free_throws', 'age', 'games_started', 'assists', 'minutes_played', 'team', 'positions', 'steals', 'offensive_rebounds', 'made_free_throws', 'games_played', 'attempted_field_goals', 'defensive_rebounds', 'made_field_goals', 'name', 'attempted_three_point_field_goals', 'made_three_point_field_goals', 'personal_fouls', 'blocks'}
import os, json, datetime
from datetime import date
SEASONS = {2018: (date(2017, 10, 18), date(2018, 6, 7))
            }

def validate_player_dict(player_dict):
    """
    raises a RuntimeException if the player dictionary contains incorrect keys 

    Args:
        player_dict: (dict)
    """
    keys = set(player_dict.keys())
    if keys != PLAYER_KEYS:
        extra = keys.difference(PLAYER_KEYS)
        missing = PLAYER_KEYS.difference(keys)
        error_msg = "Malformed player dictionary. \n"
        if extra:
            error_msg += "Player dictionary contains the following \
            extraneous keys: %s \n" % extra
        if missing:
            error_msg += "Player dictionary is missing the following \
            keys: %s" % missing
        raise RuntimeException(error_msg)

def get_box_scores(day, month, year):
    """
    returns a list of the box scores from the date provided
    Args:
        day: (int)
        month: (int)
        year: (int)
    Returns:
        (list<dict>) a list of box score dictionaries
    """
    return client.player_box_scores(day, month, year)

def get_player_totals(end_year):
    """
    returns a list of the total stats for each player for the season that ends
    in end_year
    *Note*: a player will appear once for each team they played on
    Args:
        end_year: (int)
    Returns:
        (list<dict>) a list of player dictionaries
    """
    path_to_json = "../data/players/%s_players.json" % str(end_year)
    if not os.path.exists(path_to_json):
        client.players_season_totals(end_year, output_type=OutputType.JSON,
            output_file_path=path_to_json)
    f = open(path_to_json, "r")
    return json.load(f)

def get_games(end_year):
    """
    Args:
        end_year: (int)
    Returns:
    """
    path_to_json = "../data/games/%s_games.json" % str(end_year)
    if not os.path.exists(path_to_json):
        client.season_schedule(end_year, output_type=OutputType.JSON,
            output_file_path=path_to_json)
    f = open(path_to_json, "r")
    return json.load(f)

def prune(player_dict):
    prune_list = ["age", "games_started", "team", "positions", "name"]
    for key in prune_list:
        player_dict.pop(key)

def season_league_totals(end_year):
    player_dicts = get_player_totals(end_year)
    return get_totals(player_dicts)

def season_team_totals(end_year, team):
    player_dicts = get_player_totals(end_year)
    player_dicts = [player for player in player_dicts if player["team"] == team]
    return get_totals(player_dicts)

def get_totals(player_dicts):
    totals = player_dicts[0]
    prune(totals)
    for player_dict in player_dicts[1:]:
        prune(player_dict)
        for key in totals.keys():
            assert type(totals[key] in (float, int))
            totals[key] += player_dict[key]
    add_points(totals)
    return totals 

def add_points(player_dict):
    player_dict["points"] = 3*player_dict["made_three_point_field_goals"] + \
            2* (player_dict["made_field_goals"] - player_dict["made_three_point_field_goals"]) \
            + player_dict["made_free_throws"]

"""
def range_global_totals(start_date, end_date):
"""

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


