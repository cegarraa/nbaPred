import os, json
from datetime import date, timedelta
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
PLAYER_KEYS = {'turnovers', 'attempted_free_throws', 'age', 
                'games_started', 'assists', 'minutes_played', 
                'team', 'positions', 'steals', 'offensive_rebounds', 
                'made_free_throws', 'games_played', 'attempted_field_goals', 
                'defensive_rebounds', 'made_field_goals', 'name', 
                'attempted_three_point_field_goals', 'made_three_point_field_goals', 
                'personal_fouls', 'blocks'}

BOX_SCORE_KEYS = {'assists',
                'attempted_field_goals',
                'attempted_free_throws',
                'attempted_three_point_field_goals',
                'blocks',
                'defensive_rebounds',
                'game_score',
                'location',
                'made_field_goals',
                'made_free_throws',
                'made_three_point_field_goals',
                'name',
                'offensive_rebounds',
                'opponent',
                'outcome',
                'personal_fouls',
                'seconds_played',
                'steals',
                'team',
                'turnovers'}

SEASONS = {2018: (date(2017, 10, 18), date(2018, 4, 11))
            }


def validate_dictionary(dictionary, expected_keys, dict_name):
    keys = set(dictionary.keys())
    if keys != expected_keys:
        extra = keys.difference(expected_keys)
        missing = expected_keys.difference(keys)
        error_msg = "Malformed %s. \n" % dict_name
        if extra:
            error_msg += "%s contains the following \
            extraneous keys: %s \n" % (dict_name, extra)
        if missing:
            error_msg += "%s is missing the following \
            keys: %s" % (dict_name, missing)
        raise RuntimeException(error_msg)


def validate_player_dict(player_dict):
    """
    raises a RuntimeException if the player dictionary contains incorrect keys 

    Args:
        player_dict: (dict) from output of client
    """
    validate_dictionary(player_dict, PLAYER_KEYS, "Player Dictionary")


def validate_box_score_dict(box_score_dict):
    """
    raises a RuntimeException if the box score dictionary contains incorrect keys 

    Args:
        box_score_dict: (dict) from output of client
    """
    validate_dictionary(box_score_dict, BOX_SCORE_KEYS, "Box Score Dictionary")


def get_box_scores(year, month, day):
    """
    returns a list of the box scores from the date provided
    Args:
        day: (int)
        month: (int)
        year: (int)
    Returns:
        (list<dict>) a list of box score dictionaries
    """
    str_day, str_month, str_year = str(day), str(month), str(year)
    if day < 10:
        str_day = "0" + str_day
    if month < 10:
        str_month = "0" + str_month
    date = "_".join([str_year, str_month, str_day])
    path_to_json = "../data/box_scores/%s_box_scores.json" % date
    if not os.path.exists(path_to_json):
        client.player_box_scores(day, month, year, output_type=OutputType.JSON,
            output_file_path=path_to_json)
    f = open(path_to_json, "r")
    return json.load(f)


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


def prune_player(player_dict):
    """
    prunes player_dict into a dictionary to be used in accumulating
    team or league stats
    Args:
        player_dict: (dict)
    """
    prune_list = ["age", "games_started", "team", "positions", "name"]
    prune(player_dict, prune_list)


def prune_box_score(box_score_dict):
    prune_list = ["location", "name", "opponent", "outcome", "team"]
    prune(box_score_dict, prune_list)

def prune(dictionary, prune_list):
    for key in prune_list:
        dictionary.pop(key)


def season_league_totals(end_year):
    player_dicts = get_player_totals(end_year)
    return get_totals(player_dicts)


def season_team_totals(end_year, team):
    """
    Args: 

    """
    player_dicts = get_player_totals(end_year)
    player_dicts = [player for player in player_dicts if player["team"] == team]
    return get_totals(player_dicts)


def season_opponent_totals(end_year, team):
    start_date, end_date =  SEASONS[end_year]
    totals = {key: 0 for key in BOX_SCORE_KEYS}
    prune_box_score(totals)
    for date in date_range(start_date, end_date):
        year, month, day = date.year, date.month, date.day
        box_scores = get_box_scores(year, month, day)
        for box_score in box_scores:
            validate_box_score_dict(box_score)
            if box_score["opponent"] == team:
                prune_box_score(box_score)
                for key in totals:
                    totals[key] += box_score[key]
    return totals


def get_totals(player_dicts):
    totals = player_dicts[0]
    prune_player(totals)
    for player_dict in player_dicts[1:]:
        prune_player(player_dict)
        for key in totals.keys():
            assert type(totals[key] in (float, int))
            totals[key] += player_dict[key]
    add_points(totals)
    return totals 

def add_points(player_dict):
    player_dict["points"] = 3*player_dict["made_three_point_field_goals"] + \
            2* (player_dict["made_field_goals"] - player_dict["made_three_point_field_goals"]) \
            + player_dict["made_free_throws"]


def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


