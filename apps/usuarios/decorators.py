from functools import wraps

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def es_artesano(user):
    return user.is_authenticated and hasattr(user, 'artesano')


def administrador_requerido(view_func):
    vista_staff = staff_member_required(login_url='login')(view_func)

    @wraps(view_func)
    def vista_protegida(request, *args, **kwargs):
        if request.user.is_authenticated and not es_administrador(request.user):
            raise PermissionDenied
        return vista_staff(request, *args, **kwargs)

    return vista_protegida


def artesano_requerido(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def vista_protegida(request, *args, **kwargs):
        if not es_artesano(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return vista_protegida
