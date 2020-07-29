from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import Report
from django.core.exceptions import ImproperlyConfigured
import os, json
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import datetime
from django.utils.dateformat import DateFormat

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

    return render(request, 'index.html', {'report':report, 'apiKey':API_KET})

def list(request):
    return render(request, 'list.html')

@login_required
@require_POST
def report(request):
    if request.method == "POST":
        report = Report()
        report.input_user = request.user
        if request.POST['input_report'] == '':
            report.input_report = 'Check'
        else :
            report.input_report = request.POST['input_report']
        report.input_lat = request.POST['lat']
        report.input_lon = request.POST['lon']
        report.input_date = DateFormat(datetime.now()).format('YmdHis')
        report.save()
        return HttpResponse(content_type='application/json')
