from django.shortcuts import render
from apps.stands.models import Stand

# Create your views here.
def mapa_stands(request):
    # Consulta de Stands para el mapa
    stands_qs = Stand.objects.select_related('artesano').all()
    stands_data = []
    for s in stands_qs:
        stands_data.append({
            'numero_stand': s.numero_stand,
            'ubicacion_mapa': s.ubicacion_mapa,
            'estado': s.estado,
            'artesano_nombre': s.artesano.nombre_comercial if s.artesano else None,
            'artesano_rubro': s.artesano.get_rubro_display() if s.artesano else None,
            'artesano_localidad': s.artesano.localidad if s.artesano else None,
        })

    context = {
            'stands_json': stands_data,
        }
    return render(request, 'stands/mapa_stands.html', context)