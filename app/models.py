from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Report(models.Model):
    objects = models.Manager()
    input_user = models.ForeignKey(User, on_delete = models.CASCADE)
    input_report = models.CharField(max_length=200, null = True, default='비어있음' )
    input_date = models.DateTimeField('date published', default=timezone.now)
