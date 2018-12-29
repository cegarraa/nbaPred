import utils

class Player:
    """
    a class representing a player's play for a particular team, 
    on a particular season

    Instance Attributes:
        turnovers: (int)
        attempted_free_throws: (int) 
        age: (int) 
        games_started: (int) 
        assists: (int) 
        minutes_played: (int) 
        team: (TEAM) 
        positions: (POSITION) 
        steals: (int) 
        offensive_rebounds: (int) 
        made_free_throws: (int) 
        games_played: (int) 
        attempted_field_goals: (int) 
        defensive_rebounds: (int)
        made_field_goals: (int) 
        name: (str) 
        attempted_three_point_field_goals: (int)
        made_three_point_field_goals: (int)
        personal_fouls: (int)
        blocks: (int)
    """
    def __init__(self, player_dict, year):
        """
        Args:
            player_dict: (dict)
            year: (int)
        """
        utils.validate_player_dict(player_dict)
        for key in player_dict:
            setattr(self, key, player_dict[key])
        self.end_year = year

    def __str__(self):
        return "<%s, %s, %d>" % (self.name, self.team, self.end_year)

    def __repr__(self):
        return self.__str__()

    def get_players(end_year):
        players = []
        player_dicts = utils.get_player_totals(end_year)
        for player_dict in player_dicts:
            players.append(Player(player_dict, end_year))
        return players

if  __name__ == "__main__":
    players = Player.get_players(2018)
    for p in players:
        print(p)

