from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('report/', views.report, name='report'),
    path('test/', views.test, name='test'),
    path('getApi/', views.getApi, name='getApi'),
    path('getTest/', views.getTest, name='getTest'),
]