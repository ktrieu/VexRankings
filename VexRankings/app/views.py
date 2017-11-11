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

from app.rankings import vexdb
from app.models import Team

def api_get_rankings_data(request):
    week_num = request.GET.get('week_num', None)
    if week_num == None:
        week_num = vexdb.get_num_weeks_to_today()
    else:
        week_num = int(week_num)
    ordered_teams = Team.objects.all()
    rankings_data = list()
    for team in ordered_teams:
        rankings_data.append({
            'name' : team.name,
            'elo' : team.elos[week_num - 1],
            'elo_change' : team.elo_changes[week_num - 1]
            })
    return JsonResponse({ 'data' : rankings_data })

def rankings(request):
    return render(request, 'app/rankings.html', context={'week_range' : reversed(range(vexdb.get_num_weeks_to_today()))})
