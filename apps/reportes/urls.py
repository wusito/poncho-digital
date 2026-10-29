from django.urls import path
from . import views

urlpatterns = [
    # CU-18: Reporte de artesanos.
    path('artesanos/', views.reporte_artesanos, name='reporte_artesanos'),
    # CU-19: Reporte de ocupación de stands.
    path('stands/', views.reporte_stands, name='reporte_stands'),
    # CU-20: Reporte de productos por artesano.
    path('productos/', views.reporte_productos, name='reporte_productos'),
]
