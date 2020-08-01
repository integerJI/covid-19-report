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
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize


def index(request):
    today = DateFormat(datetime.now()).format('Y-m-d')
    report = Report.objects.filter(input_user=request.user,input_date=today)

    API_KEY = getattr(settings, 'API_KEY', 'API_KEY')

    return render(request, 'index.html', {'report':report, 'apiKey':API_KEY})
    

def list(request):
    report = Report.objects.filter(input_user=request.user).order_by('-input_date')
    return render(request, 'list.html', {'report':report })

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
        report.input_date = DateFormat(datetime.now()).format('Y-m-d')
        report.input_time = DateFormat(datetime.now()).format('H:i:s')
        report.save()
        return HttpResponse(content_type='application/json')


def test(request):
    today = DateFormat(datetime.now()).format('Y-m-d')
    report = Report.objects.filter(Q(input_user=request.user),Q(input_date=today))

    # report2 = Report.objects.filter(Q(input_user=request.user),Q(input_date=today))
    # .values('input_user', 'input_report', 'input_date', 'input_time', 'input_lat', 'input_lon')
    # serialized_q = serializers.serialize('json', list(report2), fields=('input_user', 'input_report', 'input_date', 'input_time', 'input_lat', 'input_lon'))

    permission_list = Report.objects.all().order_by('-id')
    permission_serialize= json.loads(serialize('json', permission_list))
    # return JsonResponse({'data': permission_serialize})

    # rows = json.dumps(report)
    # print(rows)

    print(permission_serialize)

    API_KEY = getattr(settings, 'API_KEY', 'API_KEY')

    context = {
        'report': report, 
        'apiKey': API_KEY,
        'data': permission_serialize,
    }

    return JsonResponse(request, 'test.html', context=context)