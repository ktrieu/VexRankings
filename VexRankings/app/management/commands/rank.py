from django.core.management.base import BaseCommand, CommandError
import app.rankings.vexdb as vexdb
import app.rankings.ranker as ranker
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Ranking teams...')
        today_week_idx = vexdb.get_today_week_idx()
        vex_ranker = ranker.Ranker()
        for week_num in range(today_week_idx + 1):
            dates = vexdb.get_dates_in_week(week_num)
            self.stdout.write(f'Ranking week {week_num}. {dates[0]} to {dates[-1]}')
            vex_ranker.rank_matches_in_week(week_num)
        self.stdout.write('Ranking complete.')
        self.stdout.write('Saving...')
        vex_ranker.save_to_database()
        self.stdout.write('Complete.')