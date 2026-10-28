from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from apps.stands.models import Stand

from .forms import PostulanteArtesanoForm
from .models import Artesano, PostulanteArtesano


def registro_artesano(request):
    """
    Vista pública de registro de participación de artesanos (HU-01).
    Recibe los datos del formulario existente (PostulanteArtesanoForm / registro_artesano.html),
    guarda la solicitud en estado PENDIENTE y notifica el resultado mediante Django messages.
    """
    if request.method == 'POST':
        form = PostulanteArtesanoForm(request.POST)

        # Se adapta a la estructura existente de forms.py y registro_artesano.html,
        # donde departamento y dirección son opcionales en el modelo.
        if 'departamento' in form.fields:
            form.fields['departamento'].required = False

        if form.is_valid():
            solicitud = form.save(commit=False)
            if not solicitud.departamento:
                solicitud.departamento = None
            if not solicitud.direccion:
                solicitud.direccion = None
            solicitud.estado_solicitud = PostulanteArtesano.EstadoSolicitud.PENDIENTE
            solicitud.save()

            messages.success(
                request,
                f"¡Solicitud enviada con éxito! La postulación de '{solicitud.nombre_emprendimiento}' "
                f"fue guardada en estado PENDIENTE.",
            )
            return redirect('registro_artesano')
        else:
            dni_ingresado = request.POST.get('dni', '').strip()
            if 'dni' in form.errors and PostulanteArtesano.objects.filter(dni=dni_ingresado).exists():
                messages.error(
                    request,
                    "No se pudo enviar la solicitud: ya existe una postulación registrada con ese número de DNI.",
                )
            else:
                messages.error(
                    request,
                    "Ocurrió un error al registrar la solicitud. Por favor, verificá los datos ingresados en el formulario.",
                )
    else:
        form = PostulanteArtesanoForm()

    context = {
        'form': form,
    }
    return render(request, 'artesanos/registro_artesano.html', context)


def panel_solicitudes(request):
    """
    Vista/panel de evaluación de solicitudes de artesanos (HU-02).
    Permite listar, buscar, filtrar por estado, ver la ficha completa y aprobar o rechazar solicitudes.
    Al aprobar, requiere y asigna un stand disponible.
    """
    estado_filtro = request.GET.get('estado', '').strip().upper()
    busqueda = request.GET.get('q', '').strip()

    solicitudes_base = PostulanteArtesano.objects.select_related('usuario').all()

    total_solicitudes = solicitudes_base.count()
    total_pendientes = solicitudes_base.filter(
        estado_solicitud=PostulanteArtesano.EstadoSolicitud.PENDIENTE
    ).count()
    total_aprobadas = solicitudes_base.filter(
        estado_solicitud=PostulanteArtesano.EstadoSolicitud.APROBADO
    ).count()
    total_rechazadas = solicitudes_base.filter(
        estado_solicitud=PostulanteArtesano.EstadoSolicitud.RECHAZADO
    ).count()

    solicitudes = solicitudes_base

    estados_validos = {
        PostulanteArtesano.EstadoSolicitud.PENDIENTE,
        PostulanteArtesano.EstadoSolicitud.APROBADO,
        PostulanteArtesano.EstadoSolicitud.RECHAZADO,
    }
    if estado_filtro in estados_validos:
        solicitudes = solicitudes.filter(estado_solicitud=estado_filtro)
    else:
        estado_filtro = ''

    if busqueda:
        solicitudes = solicitudes.filter(
            Q(nombre_emprendimiento__icontains=busqueda)
            | Q(nombre__icontains=busqueda)
            | Q(apellido__icontains=busqueda)
            | Q(dni__icontains=busqueda)
            | Q(cuit_o_cuil__icontains=busqueda)
            | Q(localidad__icontains=busqueda)
            | Q(email__icontains=busqueda)
        )

    solicitudes = solicitudes.annotate(
        prioridad_estado=Case(
            When(estado_solicitud=PostulanteArtesano.EstadoSolicitud.PENDIENTE, then=Value(0)),
            When(estado_solicitud=PostulanteArtesano.EstadoSolicitud.APROBADO, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by('prioridad_estado', '-fecha_solicitud')

    context = {
        'solicitudes': solicitudes,
        'stands_disponibles': Stand.objects.filter(
            estado=Stand.EstadoStand.DISPONIBLE,
            artesano__isnull=True,
        ).order_by('numero_stand'),
        'estado_filtro': estado_filtro,
        'busqueda': busqueda,
        'total_solicitudes': total_solicitudes,
        'total_pendientes': total_pendientes,
        'total_aprobadas': total_aprobadas,
        'total_rechazadas': total_rechazadas,
    }
    return render(request, 'artesanos/panel_solicitudes.html', context)


def aprobar_solicitud(request, pk):
    """
    Aprueba una solicitud pendiente de forma atómica (HU-02):
    crea/vincula el User con DNI como username y contraseña inicial,
    crea el perfil oficial Artesano, asigna el stand seleccionado y pasa la solicitud a estado APROBADO.
    """
    if request.method != 'POST':
        return redirect('panel_solicitudes')

    postulante = get_object_or_404(PostulanteArtesano, pk=pk)
    stand_id = request.POST.get('stand_id', '').strip()

    if postulante.estado_solicitud == PostulanteArtesano.EstadoSolicitud.APROBADO:
        messages.error(
            request,
            f"La solicitud de '{postulante.nombre_emprendimiento}' ya se encuentra aprobada.",
        )
        return redirect('panel_solicitudes')

    if not stand_id.isdecimal():
        messages.error(request, "Debe seleccionar un stand disponible para aprobar la solicitud.")
        return redirect('panel_solicitudes')

    if Artesano.objects.filter(nombre_comercial__iexact=postulante.nombre_emprendimiento).exists():
        messages.error(
            request,
            f"No se pudo aprobar: ya existe un artesano oficial con el nombre comercial "
            f"'{postulante.nombre_emprendimiento}'.",
        )
        return redirect('panel_solicitudes')

    User = get_user_model()

    try:
        with transaction.atomic():
            try:
                stand = Stand.objects.select_for_update().get(
                    pk=stand_id,
                    estado=Stand.EstadoStand.DISPONIBLE,
                    artesano__isnull=True,
                )
            except Stand.DoesNotExist:
                messages.error(
                    request,
                    "No se pudo aprobar: el stand seleccionado ya no está disponible. "
                    "Actualizá el panel y seleccioná otro stand.",
                )
                return redirect('panel_solicitudes')

            if postulante.usuario:
                usuario = postulante.usuario
            else:
                usuario = User.objects.filter(username=postulante.dni).first()
                if usuario is None:
                    usuario = User.objects.create_user(
                        username=postulante.dni,
                        email=postulante.email,
                        password=postulante.dni,
                        first_name=postulante.nombre,
                        last_name=postulante.apellido,
                    )
                elif hasattr(usuario, 'artesano'):
                    messages.error(
                        request,
                        f"No se pudo aprobar: el usuario con DNI {postulante.dni} "
                        f"ya posee un perfil oficial de artesano.",
                    )
                    return redirect('panel_solicitudes')

            if hasattr(usuario, 'artesano'):
                messages.error(
                    request,
                    f"No se pudo aprobar: el usuario '{usuario.username}' ya cuenta con un perfil de artesano.",
                )
                return redirect('panel_solicitudes')

            artesano = Artesano.objects.create(
                usuario=usuario,
                nombre_comercial=postulante.nombre_emprendimiento,
                rubro=postulante.rubro_principal,
                descripcion_emprendimiento=postulante.descripcion_proceso,
                telefono=postulante.telefono,
                provincia=postulante.provincia,
                departamento=postulante.departamento or None,
                localidad=postulante.localidad,
                direccion=postulante.direccion or None,
            )

            stand.artesano = artesano
            stand.save(update_fields=['artesano', 'estado'])

            postulante.usuario = usuario
            postulante.estado_solicitud = PostulanteArtesano.EstadoSolicitud.APROBADO
            postulante.save(update_fields=['usuario', 'estado_solicitud'])

        messages.success(
            request,
            f"¡Solicitud aprobada con éxito! Se creó el perfil oficial del artesano "
            f"'{postulante.nombre_emprendimiento}' y se vinculó la cuenta con DNI {postulante.dni}.",
        )
    except IntegrityError:
        messages.error(
            request,
            "Ocurrió un error de integridad en la base de datos al intentar aprobar la solicitud.",
        )

    return redirect('panel_solicitudes')


def rechazar_solicitud(request, pk):
    """
    Rechaza una solicitud pendiente actualizando su estado a RECHAZADO (HU-02).
    """
    if request.method != 'POST':
        return redirect('panel_solicitudes')

    postulante = get_object_or_404(PostulanteArtesano, pk=pk)

    if postulante.estado_solicitud == PostulanteArtesano.EstadoSolicitud.APROBADO:
        messages.error(
            request,
            f"No se puede rechazar la solicitud de '{postulante.nombre_emprendimiento}' "
            f"porque ya fue aprobada y tiene un perfil oficial creado.",
        )
        return redirect('panel_solicitudes')

    if postulante.estado_solicitud == PostulanteArtesano.EstadoSolicitud.RECHAZADO:
        messages.error(
            request,
            f"La solicitud de '{postulante.nombre_emprendimiento}' ya se encuentra rechazada.",
        )
        return redirect('panel_solicitudes')

    postulante.estado_solicitud = PostulanteArtesano.EstadoSolicitud.RECHAZADO
    postulante.save(update_fields=['estado_solicitud'])

    messages.success(
        request,
        f"La solicitud de '{postulante.nombre_emprendimiento}' ({postulante.apellido}, {postulante.nombre}) "
        f"fue rechazada correctamente.",
    )
    return redirect('panel_solicitudes')
