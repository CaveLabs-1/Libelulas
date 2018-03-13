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

]

