from django.core.management.base import BaseCommand, CommandError
import datetime
import django.utils.dateparse as dateparse
import requests

SEASON_START = dateparse.parse_date('2017-06-04')
EVENTS_URL = 'https://api.vexdb.io/v1/get_events'
MATCHES_URL = 'https://api.vexdb.io/v1/get_matches'


class Command(BaseCommand):

    def get_events_on_dates(self, dates):
        event_params = {
                'program' : 'VRC',
                'season' : 'current'
            }
        events = list()
        for date in dates:
            event_params['date'] = date
            r = requests.get(EVENTS_URL, params=event_params).json()
            if r['status'] == 1:
                events.append(r['result'])
            else:
                error_code = r['error_code']
                raise CommandError(f'Error fetching events for {date}. Error code: {error_code}')
        return events

    def get_matches_from_sku(self, sku):
        match_params = {
                'sku' : sku
            }
        r = requests.get(MATCHES_URL, params=match_params).json()
        if r['status'] == 1:
            return r['result']
        else:
            error_code =r['error_code']
            raise CommandError(f'Error fetching matches for {sku}. Error code: {error_code}')

    def get_matches_by_week(self, week_num):
        date_start = SEASON_START + datetime.timedelta(weeks=week_num)
        date_end = date_start + datetime.timedelta(weeks=1)
        week_dates = list()
        while date_start < date_end:
            week_dates.append(date_start.isoformat())
            date_start += datetime.timedelta(days=1)
        self.stdout.write(str(self.get_events_on_dates(week_dates)))

    def handle(self, *args, **options):
        self.stdout.write('Ranking teams...')
        self.get_matches_by_week(0)