from django.urls import path
from . import views

urlpatterns = [
    path('stands/', views.mapa_stands, name='mapa_stands'),
]