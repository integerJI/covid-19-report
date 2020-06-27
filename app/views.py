# app/view.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import Report

# Create your views here.

def index(request):
    report = Report.objects.all()
 
    if request.method == "POST":
        report=Report()
        report.input_user = request.user
        report.input_report = request.POST['input_report']
        report.input_date = timezone.datetime.now()
        report.save()
        return redirect(reverse('index'))

    else:
        return render(request, 'index.html')

    return render(request, 'index.html')
