from django.urls import path
from . import views
from django.urls import path
from .views import *
from django.urls import path
from equipo.views import *

from django.urls import path

app_name = 'torneo'

urlpatterns = [
    path('crear_torneo/', views.crear_torneo, name='crear_torneo'),
    path( '' , views.lista_torneos, name='lista_torneos'),
    path('<int:torneo_id>/', views.detalle_torneo, name='detalle_torneo'),
    path('editar/<int:torneo_id>', views.editar_torneo, name='editar_torneo'),
    path('eliminar/<int:pk>', views.eliminar_torneo.as_view(), name='eliminar_torneo'),
    path('eliminar_equipo/<int:id_equipo>/<int:id_torneo>', views.eliminar_equipo, name='eliminar_equipo'),
    path('cerrar_registro/<int:id_torneo>', views.cerrar_registro, name='cerrar_registro'),
    path('mandar_codigoCedula/<int:torneo_id>/<int:jornada_id>', views.mandar_codigoCedula, name='mandar_codigoCedula'),

]
