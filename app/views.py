# app/view.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import Report
from django.core.exceptions import ImproperlyConfigured

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect

import os, json

# Create your views here.

def index(request):
    report = Report.objects.filter(input_user=request.user)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secret_file = os.path.join(BASE_DIR, 'secrets.json')

    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

    API_KET = get_secret("API_KET")

    if request.method == "POST":
        report=Report()
        report.input_user = request.user
        report.input_report = request.POST['input_report']
        report.input_date = timezone.datetime.now()
        report.save()
        return HttpResponse(content_type='application/json')

    else:
        return render(request, 'index.html', {'report':report, 'apiKey':API_KET})

