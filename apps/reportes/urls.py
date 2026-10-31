from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('gestion/', views.generar_reportes, name='generar_reportes'),
    # CU-18: Reporte de artesanos.
    path('gestion/artesanos/', views.reporte_artesanos, name='reporte_artesanos'),
    # CU-19: Reporte de ocupación de stands.
    path('gestion/stands/', views.reporte_stands, name='reporte_stands'),
    # CU-20: Reporte de productos por artesano.
    path('gestion/productos/', views.reporte_productos, name='reporte_productos'),
    # Nueva ruta de exportación a Excel
    path('gestion/exportar/excel/artesanos/', views.exportar_excel_artesanos, name='exportar_excel_artesanos'),
]
