from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Report(models.Model):
    objects = models.Manager()
    input_user = models.ForeignKey(User, on_delete = models.CASCADE)
    input_report = models.CharField(max_length=200, null = True, default='비어있음')
    input_date = models.IntegerField(default=0, null=True, blank=True)
    input_time = models.IntegerField(default=0, null=True, blank=True)
    input_lat = models.DecimalField(max_digits=9, decimal_places=6, null = True)
    input_lon = models.DecimalField(max_digits=9, decimal_places=6, null = True)

    def __str__(self):
        return '%s - %s - %s' % (self.input_user, self.input_report, self.input_date) 
