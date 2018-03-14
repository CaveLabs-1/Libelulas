from django.urls import path
from . import views
from django.urls import path
from .views import *


app_name = 'equipo'

urlpatterns = [
    path('agregar_equipo/', views.agregar_equipo, name='agregar_equipo'),
    path('', lista_equipos.as_view() , name='lista_equipos'),
    path ('<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('editar_equipo/<int:pk>/', views.editar_equipo, name='editar_equipo'),
    path('borrar_equipo/<int:pk>/', borrar_equipo.as_view(), name='borrar_equipo'),
    path ('<int:equipo_id>/eliminar_jugadora/<int:idJugadora>/', views.eliminar_jugadora, name='eliminar_jugadora'),

]
