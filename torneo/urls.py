from django.urls import path
from . import views

app_name = 'torneo'

urlpatterns = [
    path('crear_torneo/', views.crear_torneo, name='crear_torneo'),
    path( '' , views.lista_torneos, name='lista_torneos'),
    path('<int:torneo_id>/', views.detalle_torneo, name='detalle_torneo'),
    path('editar/<int:torneo_id>', views.editar_torneo, name='editar_torneo'),
    path('eliminar/<int:id_torneo>', views.eliminar_torneo, name='eliminar_torneo'),
    path('eliminar_equipo/<int:id_equipo>/<int:id_torneo>', views.eliminar_equipo, name='eliminar_equipo'),
    path('registrar_partido/<int:id_partido>', views.registrar_partido, name='registrar_partido'),
    path('cerrar_registro/<int:id_torneo>', views.cerrar_registro, name='cerrar_registro'),
    path('editar_registro/<int:id_torneo>', views.editar_registro, name='editar_registro'),
    path('carga_partidos/', views.carga_partidos, name='carga_partidos'),
    path('editar_partido/<slug:id_partido>', views.editar_partido, name='editar_partido'),
    path('mandar_codigoCedula/<int:torneo_id>/<int:jornada_id>', views.mandar_codigoCedula, name='mandar_codigoCedula'),
    path('mandar_Cedula/<slug:partido_id>', views.mandar_Cedula, name='mandar_cedula'),
    path('accesar_cedula/', views.accesar_cedula, name='accesar_cedula'),
    path('registrar_cedula/<slug:id_torneo>/<slug:id_partido>', views.registrar_cedula, name='registrar_cedula'),
    path('registrar_asistencia', views.registrar_asistencia, name='registrar_asistencia'),
    path('registrar_eventos/<slug:id_partido>', views.registrar_eventos, name='registrar_eventos'),
    path('eliminar_evento/<slug:id_partido>', views.eliminar_evento, name='eliminar_evento'),
    path('nueva_jornada/<int:id_torneo>', views.nueva_jornada, name='nueva_jornada'),
    path('nuevo_partido/<int:id_jornada>', views.nuevo_partido, name='nuevo_partido'),
    path('ganador/<int:id_torneo>', views.ganador, name='ganador'),
]
