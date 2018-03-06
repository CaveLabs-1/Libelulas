from django.urls import path
from .import views

app_name = 'administrador'

urlpatterns = [
    path('agregar_administrador/', views.agregar_administrador, name='agregar_administrador'),
    path('lista_administrador/', views.lista_administrador, name='lista_administrador'),
    path('editar_administrador/<int:id_administrador>/', views.editar_administrador, name='editar_administrador'),
]
