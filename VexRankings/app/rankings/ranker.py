from app.models import Team
import app.rankings.vexdb as vexdb

class Ranker:

    teams = dict()
    ranked_skus = set()

    def rank_matches_in_week(self, week_num):
        dates = vexdb.get_dates_in_week(week_num)
        skus = vexdb.get_skus_on_dates(dates)
        matches = list()
        for sku in skus:
            if sku not in self.ranked_skus:
                matches.extend(vexdb.get_matches_from_sku(sku))
                self.ranked_skus.add(sku)

    def rank_match(self, match, week_num):
        pass