from django.core.management.base import BaseCommand, CommandError
from app.models import Team
import app.rankings.vexdb as vexdb
import app.rankings.ranker as ranker
import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Rebuild rankings from scratch instead of just ranking the last week',
        )

    def handle(self, *args, **options):
        today_week_idx = vexdb.get_today_week_idx()
        vex_ranker = ranker.Ranker()
        if options['clean'] == True:
            self.stdout.write('Ranking teams from scratch...')
            Team.objects.all().delete()
            for week_num in range(today_week_idx + 1):
                dates = vexdb.get_dates_in_week(week_num)
                self.stdout.write(f'Ranking week {week_num}. {dates[0]} to {dates[-1]}')
                vex_ranker.rank_matches_in_week(week_num)
            self.stdout.write('Ranking complete.')
            self.stdout.write('Saving...')
            vex_ranker.save_to_database()
            self.stdout.write('Complete.')
        else:
            self.stdout.write('Updating rankings...')
            dates = vexdb.get_dates_in_week(today_week_idx)
            self.stdout.write(f'Current week is {today_week_idx}. {dates[0]} to {dates[-1]}')
            self.stdout.write('Reloading teams from database...')
            vex_ranker.reload_from_database()
            self.stdout.write('Ranking...')
            vex_ranker.rerank_week(today_week_idx)
            self.stdout.write('Saving...')
            vex_ranker.save_to_database()
            self.stdout.write('Complete.')