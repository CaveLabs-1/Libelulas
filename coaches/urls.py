from django.urls import path
from django.views.generic import TemplateView
from .import views
from .views import *

app_name = 'coaches'

urlpatterns = [
    path('pre_registro/<int:id_torneo>', views.pre_registro, name='pre_registro'),
    path('registrar_jugadora/<slug:codigo>', views.registrar_jugadora, name='registrar_jugadora'),
    path('registrar_equipo/<slug:codigo>', views.registrar_equipo, name='registrar_equipo'),
]
