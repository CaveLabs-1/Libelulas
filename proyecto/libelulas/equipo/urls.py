from django.urls import path
from .import views

app_name = 'equipo'

urlpatterns = [
    path('agregar_equipo/', views.agregar_equipo, name='agregar_equipo'),
]
