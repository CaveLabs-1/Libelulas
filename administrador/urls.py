from django.urls import path
from .import views

app_name = 'administrador'

urlpatterns = [
    #US3 Yo como super-administrador quiero registrar un administrador
    path('agregar_administrador/', views.agregar_administrador, name='agregar_administrador'),
    path('confirmar_contrasena/<int:id_administrador>/', views.confirmar_contrasena, name='confirmar_contrasena'),
    #US5 Yo como super-administrador quiero actualizar un administrador
    path('editar_administrador/<int:id_administrador>/', views.editar_administrador, name='editar_administrador'),
    #US6 Yo como super-administrador quiero eliminar un administrador
    path('eliminar_administrador/<int:id_administrador>/', views.eliminar_administrador, name='eliminar_administrador'),
    #US4 Yo como super-administrador quiero visualizar un administrador
    path('lista_administrador/', views.lista_administrador, name='lista_administrador'),
    path('lista_PreRegistro/', views.lista_PreRegistro, name='lista_PreRegistro'),
    path('eliminar_PreRegistro/<int:id_preregistro>/', views.eliminar_preregsitro, name='eliminar_PreRegistro'),
    path('aceptar_PreRegistro/<slug:id_preregistro>/', views.aceptar_PreRegistro, name='aceptar_PreRegistro'),
    path('detalle_equipo/<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('aceptar_jugadora/<int:id_jugadora>/', views.aceptar_jugadora, name='aceptar_jugadora'),
    path('eliminar_jugadora/<int:id_jugadora>/<int:id_equipo>', views.eliminar_jugadora, name='eliminar_jugadora'),
    path('aceptar_equipo/<int:id_equipo>/', views.aceptar_equipo, name='aceptar_equipo'),
    path('eliminar_equipo/<int:id_equipo>/', views.eliminar_equipo, name='eliminar_equipo'),
    path('validar_jugadoras/<int:id_equipo>/', views.validar_jugadoras, name='validar_jugadoras'),
]
