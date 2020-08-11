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

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        print(username,'/',password1,'/',password2)

        if not username:
            message = '아이디를 입력해주세요. error (01)'
            error = '00'
            print('01')
            return render(request, 'signup.html', {'message' : message,'error':error})

        if not password1:
            message = '비밀번호를 입력해주세요. error (02)'
            error = '00'
            print('02')
            return render(request, 'signup.html', {'message' : message,'error':error})

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                message = '아이디가 중복됩니다. 다시 시도해주세요. error (03)'
                error = '00'
                print('03')
                return render(request, 'signup.html', {'message' : message,'error':error})
            else:
                user = User.objects.create_user(username, password=password1)
                print('04')
                auth.login(request, user)
                return redirect('index')
        else:
            message = '비밀번호가 다릅니다. 다시 시도해주세요. error (04)'
            error = '00'
            print('05')
            return render(request, 'signup.html', {'message' : message,'error':error})
        
    return render(request, 'signup.html')

class Loginviews(LoginView):
    template_name = 'signin.html'
    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다. Id 혹은 Password를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form)
signin = Loginviews.as_view()

# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         if not username:
#             message = '아이디를 입력해주세요. error (01)'
#             return render(request, 'signin.html', {'message' : message})

#         if not password:
#             message = '비밀번호를 입력해주세요. error (01)'
#             return render(request, 'signin.html', {'message' : message})

#         if User.objects.filter(username=username).exists():
#             message = '존재하지 않는 회원입니다. 다시 시도해주세요. error (02)'
#             return render(request, 'signin.html', {'message' : message})
#         else:
#             user = User.objects.create_user(username, password=password)
#             auth.login(request, user)
#             return redirect('index')
#     else:
#         return render(request, 'signin.html')

# def signin(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
        
#         if not username:
#             message = '아이디를 입력해주세요. error (05)'
#             return render(request, 'signin.html', {'message' : message})

#         if not password:
#             message = '비밀번호를 입력해주세요. error (06)'
#             return render(request, 'signin.html', {'message' : message})

#         user = authenticate(username = username, password = password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#     else:
#         return render(request, 'signin.html')

class LogoutViews(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
signout = LogoutViews.as_view()
