from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.decorators import administrador_requerido

from .forms import StandForm
from .models import Stand


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


@administrador_requerido
def gestion_stands(request):
    if request.method == 'POST':
        form = StandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            messages.success(request, f"El stand {stand.numero_stand} se registró correctamente.")
            return redirect('gestion_stands')
    else:
        form = StandForm()

    return render(request, 'stands/gestion_stands.html', {
        'form': form,
        'stands': Stand.objects.select_related('artesano').all(),
    })


@administrador_requerido
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

    return render(request, 'stands/gestion_stands.html', {
        'form': form,
        'stands': Stand.objects.select_related('artesano').all(),
        'stand_editando': stand,
    })