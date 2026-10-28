from django.urls import path
from . import views

urlpatterns = [
    path('stands/', views.mapa_stands, name='mapa_stands'),
    path('stands/gestion/', views.gestion_stands, name='gestion_stands'),
    path('stands/<int:pk>/editar/', views.editar_stand, name='editar_stand'),
]