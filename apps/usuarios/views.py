from django.urls import reverse
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView

from .decorators import es_administrador, es_artesano
from .forms import LoginForm


class LoginView(DjangoLoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        if es_administrador(self.request.user):
            return reverse('panel_solicitudes')
        if es_artesano(self.request.user):
            return reverse('gestion_productos')
        return super().get_success_url()


class LogoutView(DjangoLogoutView):
    next_page = 'index'
