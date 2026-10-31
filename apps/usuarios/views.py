from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView

from .forms import LoginForm


class LoginView(DjangoLoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    next_page = 'index'


class LogoutView(DjangoLogoutView):
    next_page = 'index'
