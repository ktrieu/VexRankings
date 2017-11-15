"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse
from django.template import RequestContext
from django.core import serializers
from django.db.models import F
from datetime import datetime

from app.rankings import vexdb, ranker
from app.models import Team

def api_get_rankings_data(request):
    week_idx = request.GET.get('week_idx', None)
    if week_idx == None:
        week_idx = vexdb.get_today_week_idx()
    else:
        week_idx = int(week_idx)
    ordered_teams = Team.objects.all()
    rankings_data = list()
    for team in ordered_teams:
        rankings_data.append({
            'name' : team.name,
            'elo' : team.elos[week_idx],
            'elo_change' : team.elo_changes[week_idx]
            })
    return JsonResponse({ 'data' : rankings_data })

def api_predict_match(request):
    try:
        red_team1 = request.GET['red_team1']
        red_team2 = request.GET['red_team2']
        blue_team1 = request.GET['blue_team1']
        blue_team2 = request.GET['blue_team2']
        week_idx = int(request.GET['week_idx'])
    except KeyError:
        return HttpResponse(status=400)
    red_elo1 = Team.objects.get(name=red_team1).elos[week_idx]
    red_elo2 = Team.objects.get(name=red_team2).elos[week_idx]
    blue_elo1 = Team.objects.get(name=blue_team1).elos[week_idx]
    blue_elo2 = Team.objects.get(name=blue_team2).elos[week_idx]
    red_chance, blue_chance = ranker.Ranker.predict_match(red_elo1, red_elo2, blue_elo1, blue_elo2)
    return JsonResponse({'red_chance' : round(red_chance * 100, 2), 'blue_chance' : round(blue_chance * 100, 2)})


def rankings(request):
    return render(request, 'app/rankings.html', context={'week_range' : reversed(range(vexdb.get_today_week_idx() + 1))})
