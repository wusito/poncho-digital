from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # CU-18: Reporte de artesanos.
    path('artesanos/', views.reporte_artesanos, name='reporte_artesanos'),
    # CU-19: Reporte de ocupación de stands.
    path('stands/', views.reporte_stands, name='reporte_stands'),
    # CU-20: Reporte de productos por artesano.
    path('productos/', views.reporte_productos, name='reporte_productos'),
    # Nueva ruta de exportación a Excel
    path('exportar/excel/artesanos/', views.exportar_excel_artesanos, name='exportar_excel_artesanos'),
]
