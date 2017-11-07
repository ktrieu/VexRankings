"""
Definition of models.
"""

from django.db import models
import django.contrib.postgres.fields as pgfields

class Team(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    elos = pgfields.ArrayField(base_field=models.FloatField())
    elo_changes = pgfields.ArrayField(base_field=models.FloatField())
