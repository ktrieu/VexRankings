from django.core.management.base import BaseCommand, CommandError
import app.rankings.vexdb as vexdb
import app.rankings.ranker as ranker
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Ranking teams...')
        start_date = vexdb.SEASON_START
        weeks_to_today = 0
        while start_date < datetime.date.today():
            start_date += datetime.timedelta(weeks=1)
            weeks_to_today += 1
        vex_ranker = ranker.Ranker()
        for week_num in range(weeks_to_today):
            self.stdout.write(f'Ranking week {week_num}')
            vex_ranker.rank_matches_in_week(week_num)
        self.stdout.write('Ranking complete.')
        self.stdout.write('Saving...')
        vex_ranker.save_to_database()
        self.stdout.write('Complete.')