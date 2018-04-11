from django.urls import path
from .import views

app_name = 'administrador'

urlpatterns = [
    path('agregar_administrador/', views.agregar_administrador, name='agregar_administrador'),
    path('confirmar_contrasena/<int:id_administrador>/', views.confirmar_contrasena, name='confirmar_contrasena'),
    path('editar_administrador/<int:id_administrador>/', views.editar_administrador, name='editar_administrador'),
    path('eliminar_administrador/<int:id_administrador>/', views.eliminar_administrador, name='eliminar_administrador'),
    path('lista_administrador/', views.lista_administrador, name='lista_administrador'),
    path('lista_PreRegistro/', views.lista_PreRegistro, name='lista_PreRegistro'),
    path('eliminar_PreRegistro/<int:id_preregistro>/', views.eliminar_preregsitro, name='eliminar_PreRegistro'),
    path('aceptar_PreRegistro/<int:id_preregistro>/', views.aceptar_PreRegistro, name='aceptar_PreRegistro'),
]
