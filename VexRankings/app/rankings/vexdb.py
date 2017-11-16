from django.core.management.base import CommandError
import datetime
import django.utils.dateparse as dateparse
import requests

SEASON_START = dateparse.parse_date('2017-06-04')
EVENTS_URL = 'https://api.vexdb.io/v1/get_events'
MATCHES_URL = 'https://api.vexdb.io/v1/get_matches'

def make_request(url, params):
    headers = {
        'User-Agent': 'Vex Elo Rankings',
        'From': 'dragn194@gmail.com'
    }
    return requests.get(url, params=params, headers=headers)

def get_today_week_idx():
    start_date = SEASON_START
    weeks_to_today = 0
    while start_date <= datetime.date.today():
        start_date += datetime.timedelta(weeks=1)
        weeks_to_today += 1
    #subtract 1 from count to get index
    return weeks_to_today - 1

def get_skus_on_dates(dates):
    event_params = {
            'program' : 'VRC',
            'season' : 'current'
        }
    skus = list()
    for date in dates:
        event_params['date'] = date
        r = make_request(EVENTS_URL, event_params).json()
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
    r = make_request(MATCHES_URL, match_params).json()
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