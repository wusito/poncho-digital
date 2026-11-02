from django.urls import path
from . import views

urlpatterns = [
    path('mapa/', views.mapa_stands, name='mapa_stands'),
    path('gestion/', views.gestion_stands, name='gestion_stands'),
    path('<int:pk>/editar/', views.editar_stand, name='editar_stand'),
    path('<int:pk>/liberar/', views.liberar_stand, name='liberar_stand'),
    path('<int:pk>/asignar/', views.asignar_stand, name='asignar_stand'),
]