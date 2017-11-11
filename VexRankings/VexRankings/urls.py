"""
Definition of urls for VexRankings.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', app.views.rankings),
    url(r'^api/get_rankings/', app.views.api_get_rankings_data)
]
