from django.urls import reverse
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView

from .decorators import es_artesano
from .forms import LoginForm


class LoginView(DjangoLoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.has_perm('artesanos.view_postulanteartesano'):
            return reverse('panel_solicitudes')
        if user.has_perm('stands.view_stand'):
            return reverse('gestion_stands')
        if user.has_perm('artesanos.view_reports'):
            return reverse('reportes:generar_reportes')
        if es_artesano(user) and user.has_perm('productos.view_producto'):
            return reverse('gestion_productos')
        return super().get_success_url()


class LogoutView(DjangoLogoutView):
    next_page = 'index'
