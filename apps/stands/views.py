from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.artesanos.models import Artesano, PostulanteArtesano
from apps.usuarios.decorators import permisos_requeridos, verificar_permisos

from .forms import StandForm
from .models import Stand


def _gestion_stands_context(form, stand_editando=None):
    postulaciones = PostulanteArtesano.objects.filter(
        usuario_id=OuterRef('usuario_id')
    )
    context = {
        'form': form,
        'stands': Stand.objects.select_related('artesano').all(),
        'artesanos_disponibles': (
            Artesano.objects.filter(stand_asignado__isnull=True)
            .select_related('usuario')
            .annotate(
                nombre=Subquery(postulaciones.values('nombre')[:1]),
                apellido=Subquery(postulaciones.values('apellido')[:1]),
                dni=Subquery(postulaciones.values('dni')[:1]),
                cuit=Subquery(postulaciones.values('cuit_o_cuil')[:1]),
            )
        ),
        'rubros_artesanos': Artesano._meta.get_field('rubro').choices,
    }
    if stand_editando is not None:
        context['stand_editando'] = stand_editando
    return context


def mapa_stands(request):
    stands_qs = Stand.objects.select_related('artesano').all()
    stands_data = [
        {
            'numero_stand': stand.numero_stand,
            'ubicacion_mapa': stand.ubicacion_mapa,
            'estado': stand.estado,
            'estado_display': stand.get_estado_display(),
            'artesano_nombre': stand.artesano.nombre_comercial if stand.artesano else None,
            'artesano_rubro': (
                stand.artesano.get_rubro_display() if stand.artesano else None
            ),
            'artesano_localidad': stand.artesano.localidad if stand.artesano else None,
        }
        for stand in stands_qs
    ]
    context = {'stands_json': stands_data}
    return render(request, 'stands/mapa_stands.html', context)


@permisos_requeridos('stands.view_stand')
def gestion_stands(request):
    if request.method == 'POST':
        verificar_permisos(request, 'stands.add_stand')
        form = StandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            messages.success(request, f"El stand {stand.numero_stand} se registró correctamente.")
            return redirect('gestion_stands')
    else:
        form = StandForm()

    return render(
        request,
        'stands/gestion_stands.html',
        _gestion_stands_context(form),
    )


@permisos_requeridos('stands.change_stand')
def editar_stand(request, pk):
    stand = get_object_or_404(Stand, pk=pk)
    if request.method == 'POST':
        form = StandForm(request.POST, instance=stand)
        if form.is_valid():
            stand = form.save()
            messages.success(request, f"El stand {stand.numero_stand} se actualizó correctamente.")
            return redirect('gestion_stands')
    else:
        form = StandForm(instance=stand)

    return render(
        request,
        'stands/gestion_stands.html',
        _gestion_stands_context(form, stand_editando=stand),
    )


@permisos_requeridos('stands.release_stand')
@require_POST
def liberar_stand(request, pk):
    with transaction.atomic():
        stand = get_object_or_404(Stand.objects.select_for_update(), pk=pk)
        if stand.estado != Stand.EstadoStand.ASIGNADO:
            messages.error(
                request,
                f"El stand {stand.numero_stand} no está asignado y no se puede liberar.",
            )
            return redirect('gestion_stands')

        stand.artesano = None
        stand.estado = Stand.EstadoStand.DISPONIBLE
        stand.save(update_fields=['artesano', 'estado'])

    messages.success(request, f"El stand {stand.numero_stand} se liberó correctamente.")
    return redirect('gestion_stands')


@permisos_requeridos('stands.assign_stand')
@require_POST
def asignar_stand(request, pk):
    artesano_id = request.POST.get('artesano_id', '').strip()
    if not artesano_id.isdecimal():
        messages.error(request, "Seleccioná un artesano disponible para asignar el stand.")
        return redirect('gestion_stands')

    try:
        with transaction.atomic():
            stand = Stand.objects.select_for_update().get(
                pk=pk,
                estado=Stand.EstadoStand.DISPONIBLE,
                artesano__isnull=True,
            )
            artesano = Artesano.objects.select_for_update().get(pk=int(artesano_id))
            if Stand.objects.filter(artesano=artesano).exists():
                messages.error(request, "El artesano seleccionado ya tiene un stand asignado.")
                return redirect('gestion_stands')

            stand.artesano = artesano
            stand.estado = Stand.EstadoStand.ASIGNADO
            stand.save(update_fields=['artesano', 'estado'])
    except Stand.DoesNotExist:
        messages.error(request, "El stand ya no está disponible para asignar.")
        return redirect('gestion_stands')
    except Artesano.DoesNotExist:
        messages.error(request, "El artesano seleccionado ya no está disponible para asignar.")
        return redirect('gestion_stands')
    except IntegrityError:
        messages.error(
            request,
            "No se pudo asignar el stand porque el artesano o el stand ya fueron asignados.",
        )
        return redirect('gestion_stands')

    messages.success(
        request,
        f"El stand {stand.numero_stand} se asignó correctamente a "
        f"{artesano.nombre_comercial}.",
    )
    return redirect('gestion_stands')