from decimal import Decimal

from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from apps.usuarios.decorators import administrador_requerido

from apps.artesanos.models import Artesano, RUBROS_CHOICES
from apps.productos.models import Producto
from apps.stands.models import Stand

import openpyxl
from django.http import HttpResponse
from apps.artesanos.models import Artesano

RUBROS_DICT = dict(RUBROS_CHOICES)
ESTADOS_STAND_DICT = dict(Stand.EstadoStand.choices)
CATEGORIAS_DICT = dict(Producto.CATEGORIAS)


# CU-18: Reporte de artesanos (general, por localidad y por rubro).
def _contexto_reporte_artesanos(request):
    localidad_filtro = request.GET.get('localidad', '').strip()
    rubro_filtro = request.GET.get('rubro', '').strip()

    artesanos_qs = Artesano.objects.all()

    if localidad_filtro:
        artesanos_qs = artesanos_qs.filter(localidad__iexact=localidad_filtro)
    if rubro_filtro in RUBROS_DICT:
        artesanos_qs = artesanos_qs.filter(rubro=rubro_filtro)
    else:
        rubro_filtro = ''

    artesanos = [
        {
            'id': a['id'],
            'nombre_comercial': a['nombre_comercial'],
            'rubro': a['rubro'],
            'rubro_display': RUBROS_DICT.get(a['rubro'], a['rubro']),
            'provincia': a['provincia'],
            'departamento': a['departamento'] or '-',
            'localidad': a['localidad'],
            'telefono': a['telefono'],
            'stand': a['stand_asignado__numero_stand'] or 'Sin asignar',
            'cantidad_productos': a['cantidad_productos'],
        }
        for a in artesanos_qs.annotate(
            cantidad_productos=Count('productos', distinct=True),
        ).values(
            'id',
            'nombre_comercial',
            'rubro',
            'provincia',
            'departamento',
            'localidad',
            'telefono',
            'stand_asignado__numero_stand',
            'cantidad_productos',
        ).order_by('nombre_comercial')
    ]

    por_localidad = list(
        artesanos_qs.values('localidad')
        .annotate(total=Count('id'))
        .order_by('-total', 'localidad')
    )

    por_rubro = [
        {
            'rubro': r['rubro'],
            'rubro_display': RUBROS_DICT.get(r['rubro'], r['rubro']),
            'total': r['total'],
        }
        for r in artesanos_qs.values('rubro')
        .annotate(total=Count('id'))
        .order_by('-total', 'rubro')
    ]

    localidades_disponibles = list(
        Artesano.objects.order_by('localidad')
        .values_list('localidad', flat=True)
        .distinct()
    )
    rubros_disponibles = [
        {'valor': clave, 'etiqueta': etiqueta} for clave, etiqueta in RUBROS_CHOICES
    ]

    context = {
        'artesanos': artesanos,
        'total_artesanos': len(artesanos),
        'por_localidad': por_localidad,
        'por_rubro': por_rubro,
        'localidad_filtro': localidad_filtro,
        'rubro_filtro': rubro_filtro,
        'localidades_disponibles': localidades_disponibles,
        'rubros_disponibles': rubros_disponibles,
    }
    return context


# CU-19: Reporte de ocupación de stands (disponibles vs. ocupados).
def _contexto_reporte_stands(request):
    estado_filtro = request.GET.get('estado', '').strip()

    conteo_estados = {
        fila['estado']: fila['total']
        for fila in Stand.objects.values('estado').annotate(total=Count('id'))
    }

    total_stands = sum(conteo_estados.values())
    disponibles = conteo_estados.get(Stand.EstadoStand.DISPONIBLE, 0)
    ocupados = conteo_estados.get(Stand.EstadoStand.ASIGNADO, 0)
    mantenimiento = conteo_estados.get(Stand.EstadoStand.MANTENIMIENTO, 0)

    porcentaje_ocupacion = round((ocupados / total_stands) * 100, 2) if total_stands else 0
    porcentaje_disponibles = round((disponibles / total_stands) * 100, 2) if total_stands else 0

    por_estado = [
        {
            'estado': clave,
            'estado_display': etiqueta,
            'total': conteo_estados.get(clave, 0),
        }
        for clave, etiqueta in Stand.EstadoStand.choices
    ]

    stands_qs = Stand.objects.all()
    if estado_filtro in ESTADOS_STAND_DICT:
        stands_qs = stands_qs.filter(estado=estado_filtro)
    else:
        estado_filtro = ''

    stands = [
        {
            'numero_stand': s['numero_stand'],
            'ubicacion_mapa': s['ubicacion_mapa'],
            'estado': s['estado'],
            'estado_display': ESTADOS_STAND_DICT.get(s['estado'], s['estado']),
            'artesano': s['artesano__nombre_comercial'] or '-',
            'rubro_display': RUBROS_DICT.get(s['artesano__rubro'], '-') if s['artesano__rubro'] else '-',
            'localidad': s['artesano__localidad'] or '-',
        }
        for s in stands_qs.values(
            'numero_stand',
            'ubicacion_mapa',
            'estado',
            'artesano__nombre_comercial',
            'artesano__rubro',
            'artesano__localidad',
        ).order_by('numero_stand')
    ]

    context = {
        'total_stands': total_stands,
        'disponibles': disponibles,
        'ocupados': ocupados,
        'mantenimiento': mantenimiento,
        'porcentaje_ocupacion': porcentaje_ocupacion,
        'porcentaje_disponibles': porcentaje_disponibles,
        'por_estado': por_estado,
        'stands': stands,
        'estado_filtro': estado_filtro,
        'estados_disponibles': [
            {'valor': clave, 'etiqueta': etiqueta} for clave, etiqueta in Stand.EstadoStand.choices
        ],
    }
    return context


# CU-20: Reporte de productos publicados organizados por artesano.
def _contexto_reporte_productos(request):
    artesano_filtro = request.GET.get('artesano', '').strip()
    categoria_filtro = request.GET.get('categoria', '').strip()

    productos_qs = Producto.objects.all()

    if artesano_filtro.isdigit():
        productos_qs = productos_qs.filter(artesano_id=int(artesano_filtro))
    else:
        artesano_filtro = ''

    if categoria_filtro in CATEGORIAS_DICT:
        productos_qs = productos_qs.filter(categoria=categoria_filtro)
    else:
        categoria_filtro = ''

    valor_item = ExpressionWrapper(
        F('stock') * F('precio_unitario'),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )
    cero_decimal = Value(Decimal('0.00'), output_field=DecimalField(max_digits=14, decimal_places=2))

    resumen_por_artesano = list(
        productos_qs.values(
            'artesano_id',
            'artesano__nombre_comercial',
            'artesano__rubro',
            'artesano__localidad',
        )
        .annotate(
            cantidad_productos=Count('id'),
            stock_total=Coalesce(Sum('stock'), 0),
            valor_inventario=Coalesce(Sum(valor_item), cero_decimal),
        )
        .order_by('artesano__nombre_comercial')
    )

    productos_por_artesano = {}
    for p in productos_qs.values(
        'id',
        'artesano_id',
        'nombre',
        'categoria',
        'subcategoria',
        'stock',
        'precio_unitario',
        'fecha_creacion',
    ).order_by('artesano__nombre_comercial', 'nombre'):
        productos_por_artesano.setdefault(p['artesano_id'], []).append({
            'id': p['id'],
            'nombre': p['nombre'],
            'categoria': p['categoria'],
            'categoria_display': CATEGORIAS_DICT.get(p['categoria'], p['categoria']),
            'subcategoria': p['subcategoria'] or '-',
            'stock': p['stock'],
            'precio_unitario': p['precio_unitario'],
            'fecha_creacion': p['fecha_creacion'],
        })

    reporte = [
        {
            'artesano_id': fila['artesano_id'],
            'nombre_comercial': fila['artesano__nombre_comercial'],
            'rubro_display': RUBROS_DICT.get(fila['artesano__rubro'], fila['artesano__rubro']),
            'localidad': fila['artesano__localidad'],
            'cantidad_productos': fila['cantidad_productos'],
            'stock_total': fila['stock_total'],
            'valor_inventario': fila['valor_inventario'],
            'productos': productos_por_artesano.get(fila['artesano_id'], []),
        }
        for fila in resumen_por_artesano
    ]

    totales = productos_qs.aggregate(
        total_productos=Count('id'),
        stock_general=Coalesce(Sum('stock'), 0),
        valor_general=Coalesce(Sum(valor_item), cero_decimal),
    )

    por_categoria = [
        {
            'categoria': c['categoria'],
            'categoria_display': CATEGORIAS_DICT.get(c['categoria'], c['categoria']),
            'total': c['total'],
        }
        for c in productos_qs.values('categoria')
        .annotate(total=Count('id'))
        .order_by('-total', 'categoria')
    ]

    artesanos_sin_productos = []
    if not artesano_filtro and not categoria_filtro:
        artesanos_sin_productos = list(
            Artesano.objects.annotate(cantidad=Count('productos'))
            .filter(cantidad=0)
            .values('id', 'nombre_comercial', 'localidad')
            .order_by('nombre_comercial')
        )

    context = {
        'reporte': reporte,
        'total_artesanos_con_productos': len(reporte),
        'total_productos': totales['total_productos'],
        'stock_general': totales['stock_general'],
        'valor_general': totales['valor_general'],
        'por_categoria': por_categoria,
        'artesanos_sin_productos': artesanos_sin_productos,
        'artesano_filtro': artesano_filtro,
        'categoria_filtro': categoria_filtro,
        'artesanos_disponibles': list(
            Artesano.objects.values('id', 'nombre_comercial').order_by('nombre_comercial')
        ),
        'categorias_disponibles': [
            {'valor': clave, 'etiqueta': etiqueta} for clave, etiqueta in Producto.CATEGORIAS
        ],
    }
    return context

@administrador_requerido
def generar_reportes(request):
    context = {}
    context.update(_contexto_reporte_artesanos(request))
    context.update(_contexto_reporte_productos(request))
    context.update(_contexto_reporte_stands(request))
    return render(request, 'reportes/generar_reportes.html', context)


@administrador_requerido
def reporte_artesanos(request):
    context = _contexto_reporte_artesanos(request)
    return render(request, 'reportes/reporte_artesanos.html', context)


@administrador_requerido
def reporte_stands(request):
    context = _contexto_reporte_stands(request)
    return render(request, 'reportes/reporte_stands.html', context)


@administrador_requerido
def reporte_productos(request):
    context = _contexto_reporte_productos(request)
    return render(request, 'reportes/reporte_productos.html', context)

@administrador_requerido
def exportar_excel_artesanos(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte Artesanos"

    encabezados = ['ID', 'Nombre Comercial', 'Rubro', 'Provincia', 'Departamento', 'Localidad', 'Teléfono']
    ws.append(encabezados)

    for a in Artesano.objects.all().order_by('nombre_comercial'):
        ws.append([a.id, a.nombre_comercial, a.rubro, a.provincia, a.departamento, a.localidad, a.telefono])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_artesanos.xlsx"'
    wb.save(response)
    return response