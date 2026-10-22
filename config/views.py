from django.shortcuts import render
from apps.stands.models import Stand
from apps.artesanos.models import Artesano
from apps.productos.models import Producto

def index(request):
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

    # Consulta unificada para la búsqueda de Artesanos y Productos
    busqueda_data = []
    
    # Artesanos
    for a in Artesano.objects.all():
        stand = getattr(a, 'stand_asignado', None)
        busqueda_data.append({
            'tipo': 'Artesano',
            'nombre': a.nombre_comercial,
            'rubro': a.rubro,
            'rubro_display': a.get_rubro_display(),
            'localidad': a.localidad,
            'detalle': a.descripcion_emprendimiento,
            'stand': stand.numero_stand if stand else 'Sin asignar'
        })

    # Productos
    for p in Producto.objects.select_related('artesano').all():
        stand = getattr(p.artesano, 'stand_asignado', None)
        busqueda_data.append({
            'tipo': 'Producto',
            'nombre': p.nombre,
            'categoria': p.categoria,
            'rubro_display': p.get_categoria_display(),
            'localidad': p.artesano.localidad,
            'detalle': p.descripcion,
            'stand': stand.numero_stand if stand else 'Sin asignar'
        })

    context = {
        'stands_json': stands_data,
        'busqueda_json': busqueda_data,
    }
    return render(request, 'index.html', context)