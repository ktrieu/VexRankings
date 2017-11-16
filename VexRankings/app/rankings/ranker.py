from app.models import Team
import app.rankings.vexdb as vexdb
import math

class Ranker:

    K_FACTOR = 32

    teams = dict()
    ranked_skus = set()

    def reload_from_database(self):
        for team in Team.objects.all():
            self.teams[team.name] = team

    def get_playing_team_names(self, match):
        red_teams = [match['red1'], match['red2']]
        blue_teams = [match['blue1'], match['blue2']]
        if match.get('redsit', None) != None:
            red_teams.append(match['red3'])
            red_teams.remove(match['redsit'])
        if match.get('bluesit', None) != None:
            blue_teams.append(match['blue3'])
            blue_teams.remove(match['bluesit'])
        return red_teams, blue_teams

    def add_team(self, name, week_num):
        new_team = Team(name=name)
        new_team.elos = list()
        new_team.elos[0:week_num] = [1500] * week_num
        self.teams[name] = new_team

    def update_latest_elo(self, team, week_num):
        if len(team.elos) == week_num:
            team.elos.append(team.elos[-1])
        else:
            team.elos[week_num] = team.elos[week_num - 1]

    def calc_alliance_elo(team_elo1, team_elo2):
        return (team_elo1 + team_elo2) / 2

    def predict_match(red_elo1, red_elo2, blue_elo1, blue_elo2):
        red_elo = Ranker.calc_alliance_elo(red_elo1, red_elo2)
        blue_elo = Ranker.calc_alliance_elo(blue_elo1, blue_elo2)
        #transform elos according to the elo formula
        red_elo = math.pow(10, red_elo / 400)
        blue_elo = math.pow(10, blue_elo / 400)
        #get expected results
        red_expected = red_elo / (red_elo + blue_elo)
        blue_expected = blue_elo / (red_elo + blue_elo)
        return red_expected, blue_expected

    def apply_elo(self, team1, team2, change, week_num):
        contrib1 = team1.elos[week_num] / (team1.elos[week_num] + team2.elos[week_num])
        contrib2 = team2.elos[week_num] / (team1.elos[week_num] + team2.elos[week_num])
        team1.elos[week_num] += (change * contrib1)
        team2.elos[week_num] += (change * contrib2)

    def calc_margin_adjust(self, red_score, blue_score):
        margin = math.fabs(red_score - blue_score)
        if margin == 0:
            return 1
        else:
            return math.log(margin, 10) + 1

    def rerank_week(self, week_num):
        for team in self.teams.values():
            team.elos[week_num] = team.elos[week_num - 1]
        self.rank_matches_in_week(week_num)

    def rank_matches_in_week(self, week_num):
        dates = vexdb.get_dates_in_week(week_num)
        skus = vexdb.get_skus_on_dates(dates)
        matches = list()
        ranked_teams = set()
        for sku in skus:
            if sku not in self.ranked_skus:
                matches.extend(vexdb.get_matches_from_sku(sku))
                self.ranked_skus.add(sku)
        for match in matches:
            #skip unscored matches
            if int(match['scored']) == 0:
                continue
            red_names, blue_names = self.get_playing_team_names(match)
            for name in red_names + blue_names:
                if name not in self.teams.keys():
                    self.add_team(name, week_num)
            red_team1 = self.teams[red_names[0]]
            red_team2 = self.teams[red_names[1]]
            blue_team1 = self.teams[blue_names[0]]
            blue_team2 = self.teams[blue_names[1]]
            for team in [red_team1, red_team2, blue_team1, blue_team2]:
                if team not in ranked_teams:
                    self.update_latest_elo(team, week_num)
                    ranked_teams.add(team)
            self.rank_match(red_team1, red_team2, blue_team1, blue_team2, match, week_num)
        for team in self.teams.values():
            if team not in ranked_teams:
                self.update_latest_elo(team, week_num)

    def rank_match(self, red_team1, red_team2, blue_team1, blue_team2, match, week_num):
        red_expected, blue_expected = Ranker.predict_match(red_team1.elos[week_num], red_team2.elos[week_num],
                                                         blue_team1.elos[week_num], blue_team2.elos[week_num])
        red_actual = 0
        blue_actual = 0
        if match['redscore'] > match['bluescore']:
            #red wins
            red_actual = 1
            blue_actual = 0
        elif match['redscore'] < match['bluescore']:
            #blue wins
            red_actual = 0
            blue_actual = 1
        else:
            #we have a tie
            red_actual = 0.5
            blue_actual = 0.5
        margin_adjust = self.calc_margin_adjust(match['redscore'], match['bluescore'])
        red_change = margin_adjust * self.K_FACTOR * (red_actual - red_expected)
        blue_change = margin_adjust * self.K_FACTOR * (blue_actual - blue_expected)
        self.apply_elo(red_team1, red_team2, red_change, week_num)
        self.apply_elo(blue_team1, blue_team2, blue_change, week_num)

    def save_to_database(self):
        for team in self.teams.values():
            team.calculate_changes()
            team.save()
