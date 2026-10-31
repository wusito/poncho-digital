from django.urls import path
from . import views

urlpatterns = [
    path('mapa/', views.mapa_stands, name='mapa_stands'),
    path('gestion/', views.gestion_stands, name='gestion_stands'),
    path('<int:pk>/editar/', views.editar_stand, name='editar_stand'),
]