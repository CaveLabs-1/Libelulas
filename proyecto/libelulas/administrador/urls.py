from django.urls import path
from .import views

app_name = 'administrador'

urlpatterns = [
    path('agregar_administrador/', views.agregar_administrador, name='agregar_administrador'),
]
