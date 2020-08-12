from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, '이미 존재하는 회원입니다.')
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(username, password=password1)
                auth.login(request, user)
                return redirect('index')
        else:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'signup.html')
        
    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if User.objects.filter(username=username).exists():
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, '비밀번호를 다시 입력해주세요.')
                return render(request, 'signin.html')
        else:
            messages.info(request, '존재하지 않는 회원입니다.')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

class LogoutViews(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
signout = LogoutViews.as_view()
