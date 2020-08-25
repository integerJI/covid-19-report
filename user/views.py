from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import resolve_url
from django.core.exceptions import ValidationError
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
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, '이미 존재하는 회원입니다.')
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(username, password=password1, email=email)
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

class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        print("form_valid 진입")
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            print("form_save")
            return super().form_valid(form)
        else:
            print("메일 전송 실패")
            return render(self.request, 'password_reset_done_fail.html')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        print('dispatch 시작')
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            print('self.user is not None 시작')
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                print('token == INTERNAL_RESET_URL_TOKEN 시작')
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    print('self.token_generator.check_token(self.user, session_token) 시작')
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                print('token == INTERNAL_RESET_URL_TOKEN 아닐경우 시작')
                if self.token_generator.check_token(self.user, token):
                    print('self.token_generator.check_token(self.user, token) 시작')
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        print('dispatch 끝')
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            print('get_user try')
            # urlsafe_base64_decode() decodes to bytestring
            # uid = urlsafe_base64_decode(uidb64).decode() 2020-08-25 django 2.0 + 부터는 uid에 decode 할 필요가 없어졌다고 해서 삭제
            uid = urlsafe_base64_decode(uidb64)
            
            print(uid,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            user = UserModel._default_manager.get(pk=uid)
            print(user,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
            print('user = None')
        return user

    def get_form_kwargs(self):
        print('get_form_kwargs')
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        print('form_valid')
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            print('self.post_reset_login')
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        print('get_context_data 시작')
        context = super().get_context_data(**kwargs)
        if self.validlink:
            print('self.validlink')
            context['validlink'] = True
        else:
            print('self.validlink 아닐경우')
            context.update({
                'form': None,
                'validlink': False,
            })
        return context

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context
