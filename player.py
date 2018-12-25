from basketball_reference_web_scraper import client

def get_box_scores(day, month, year):
    """
    @param day: (type=int)
    @param month: (type=int)
    @param year: (type=int)
    @return: (type=list<dict>) a list of player dictionaries
    """
    return client.player_box_scores(day, month, year)

def get_player_totals(end_year):
    return client.players_season_totals(end_year)

class Player:
    def __init__(self, player_dict, year):
        for key in player_dict:
            setattr(self, key, player_dict[key])
        self.year = year

    def __str__(self):
        return "<%s, %s, %d>" % (self.name, self.team, self.year)

    def get_players(end_year):
        players = []
        player_dicts = get_player_totals(end_year)
        for player_dict in player_dicts:
            players.append(Player(player_dict, end_year))
        return players

if  __name__ == "__main__":
    players = Player.get_players(2018)
    for p in players:
        print(p)

