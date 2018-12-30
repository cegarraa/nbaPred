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
        end_year: (int)
    """
    def __init__(self, player_dict, year, start_date=None, end_date=None):
        """
        Args:
            player_dict: (dict)
            year: (int)
        """
        self.player_dict = player_dict
        utils.validate_player_dict(player_dict)
        for key in player_dict:
            setattr(self, key, player_dict[key])
        self.end_year = year
        self.points = 3*self.made_three_point_field_goals + \
            2* (self.made_field_goals - self.made_three_point_field_goals) \
            + self.made_free_throws

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

    def per(self):
        return self.easy_per()

    def easy_per(self):
        team = utils.season_team_totals(self.end_year, self.team)
        league = utils.season_league_totals(self.end_year)
        team_ast = team["assists"]
        team_fg = team["attempted_field_goals"]
        lg_PTS = league["points"]
        lg_FGA = league["attempted_field_goals"]
        lg_ORB = league["offensive_rebounds"]
        lg_TOV = league["turnovers"]
        lg_FT = league["made_free_throws"]
        lg_FG = league["made_field_goals"]
        lg_FTA = league["attempted_free_throws"]
        lg_PF = league["personal_fouls"]
        lg_AST = league["assists"]
        factor = (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))
        VOP = lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)
        TOV = self.turnovers
        DRB_ratio = league["defensive_rebounds"] / (league["defensive_rebounds"] + league["offensive_rebounds"]) 
        return (1/ self.minutes_played) \
            * (self.made_three_point_field_goals \
            + (2/3)*self.assists \
            + (2 - factor*(team_ast/team_fg)) * self.attempted_field_goals \
            + (self.made_free_throws*.5*(1 + (1- (team_ast/team_fg)))+(2/3)*(team_ast/team_fg)) \
            - VOP * TOV \
            - VOP * DRB_ratio * (self.attempted_field_goals - self.made_field_goals) \
            - VOP * .44 * (.44 + (.56*DRB_ratio)) * (self.attempted_field_goals - self.made_field_goals) \
            + VOP * (1 - DRB_ratio)*self.defensive_rebounds \
            + VOP * DRB_ratio * self.offensive_rebounds \
            + VOP * self.steals \
            + VOP * DRB_ratio * self.blocks \
            - self.personal_fouls * ((lg_FT / lg_FG) - .44 * (lg_FTA / lg_PF) * VOP))


if  __name__ == "__main__":
    players = Player.get_players(2018)
    for p in players:
        print(p.name, p.easy_per())

