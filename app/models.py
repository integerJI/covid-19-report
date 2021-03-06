# app/modes.py

from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    objects = models.Manager()
    input_user = models.ForeignKey(User, on_delete = models.CASCADE)
    input_report = models.CharField(max_length=200, null = True, default='비어있음')
    input_date = models.CharField(max_length=20, default=0, null=True, blank=True)
    input_time = models.CharField(max_length=20, default=0, null=True, blank=True)
    input_lat = models.DecimalField(max_digits=9, decimal_places=6, null = True)
    input_lon = models.DecimalField(max_digits=9, decimal_places=6, null = True)