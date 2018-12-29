from basketball_reference_web_scraper import client
PLAYER_KEYS = {'turnovers', 'attempted_free_throws', 'age', 'games_started', 'assists', 'minutes_played', 'team', 'positions', 'steals', 'offensive_rebounds', 'made_free_throws', 'games_played', 'attempted_field_goals', 'defensive_rebounds', 'made_field_goals', 'name', 'attempted_three_point_field_goals', 'made_three_point_field_goals', 'personal_fouls', 'blocks'}

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
    return client.players_season_totals(end_year)

def get_games(end_year):
    """
    Args:
        end_year: (int)
    Returns:
    """
    return client.season_schedule(end_year)