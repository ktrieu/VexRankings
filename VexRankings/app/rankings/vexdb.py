from django.core.management.base import CommandError
import datetime
import django.utils.dateparse as dateparse
import requests

SEASON_START = dateparse.parse_date('2017-06-04')
EVENTS_URL = 'https://api.vexdb.io/v1/get_events'
MATCHES_URL = 'https://api.vexdb.io/v1/get_matches'

def get_num_weeks_to_today():
    start_date = SEASON_START
    weeks_to_today = 0
    while start_date <= datetime.date.today():
        start_date += datetime.timedelta(weeks=1)
        weeks_to_today += 1
    return weeks_to_today

def get_skus_on_dates(dates):
    event_params = {
            'program' : 'VRC',
            'season' : 'current'
        }
    skus = list()
    for date in dates:
        event_params['date'] = date
        r = requests.get(EVENTS_URL, params=event_params).json()
        if r['status'] == 1:
            for event in r['result']:
                skus.append(event['sku'])
        else:
            error_code = r['error_code']
            raise CommandError(f'Error fetching events for {date}. Error code: {error_code}')
    return skus

def get_matches_from_sku(sku):
    match_params = {
            'sku' : sku
        }
    r = requests.get(MATCHES_URL, params=match_params).json()
    if r['status'] == 1:
        return r['result']
    else:
        error_code = r['error_code']
        raise CommandError(f'Error fetching matches for {sku}. Error code: {error_code}')

def get_dates_in_week(week_num):
    date_start = SEASON_START + datetime.timedelta(weeks=week_num)
    date_end = date_start + datetime.timedelta(weeks=1)
    week_dates = list()
    while date_start < date_end:
        week_dates.append(date_start.isoformat())
        date_start += datetime.timedelta(days=1)
    return week_dates