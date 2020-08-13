# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('report/', views.report, name='report'),
    path('getApi/', views.getApi, name='getApi'),
    path('apiTest/', views.apiTest, name='apiTest'),
    path('mapTest/', views.mapTest, name='mapTest'),
    path('jsTest/', views.jsTest, name='jsTest'),
]