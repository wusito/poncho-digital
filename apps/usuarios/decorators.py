from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def es_artesano(user):
    return user.is_authenticated and hasattr(user, 'artesano')


def verificar_permisos(request, *permisos):
    if not request.user.has_perms(permisos):
        raise PermissionDenied


def permisos_requeridos(*permisos):
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def vista_protegida(request, *args, **kwargs):
            verificar_permisos(request, *permisos)
            return view_func(request, *args, **kwargs)

        return vista_protegida

    return decorador


def artesano_requerido(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def vista_protegida(request, *args, **kwargs):
        if not es_artesano(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return vista_protegida
