from django.urls import path
from . import views

urlpatterns = [
    path('gestion/', views.gestion_productos, name='gestion_productos'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]