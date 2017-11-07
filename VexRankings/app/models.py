"""
Definition of models.
"""

from django.db import models
import django.contrib.postgres.fields as pgfields

class Team(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    elos = pgfields.ArrayField(base_field=models.FloatField())
    elo_changes = pgfields.ArrayField(base_field=models.FloatField())

    def calculate_changes(self):
        self.elo_changes = list()
        #no change for the first week
        self.elo_changes.append(0)
        for i in range(1, len(self.elos)):
            self.elo_changes.append(self.elos[i] - self.elos[i -1])

    def __str__(self):
        return self.name

