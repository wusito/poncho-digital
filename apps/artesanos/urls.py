from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_artesano, name='registro_artesano'),
    path('solicitudes/', views.panel_solicitudes, name='panel_solicitudes'),
    path('solicitudes/<int:pk>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitudes/<int:pk>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
]
