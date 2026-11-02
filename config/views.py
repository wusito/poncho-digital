from django.shortcuts import render
from apps.artesanos.models import Artesano
from apps.productos.models import Producto

def index(request):
    # Consulta unificada para la búsqueda de Artesanos y Productos
    busqueda_data = []
    
    # Artesanos
    for a in Artesano.objects.filter(
        stand_asignado__isnull=False
    ).select_related('stand_asignado'):
        stand = a.stand_asignado
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
    for p in Producto.objects.filter(
        artesano__stand_asignado__isnull=False
    ).select_related('artesano', 'artesano__stand_asignado'):
        stand = p.artesano.stand_asignado
        busqueda_data.append({
            'tipo': 'Producto',
            'nombre': p.nombre,
            'categoria': p.categoria,
            'subcategoria': p.subcategoria,
            'rubro_artesano': p.artesano.rubro,
            'artesano_nombre': p.artesano.nombre_comercial,
            'rubro_display': p.get_categoria_display(),
            'localidad': p.artesano.localidad,
            'detalle': p.descripcion,
            'stand': stand.numero_stand if stand else 'Sin asignar'
        })

    context = {
        'busqueda_json': busqueda_data,
        'rubros_artesanos': Artesano._meta.get_field('rubro').choices,
    }
    return render(request, 'index.html', context)