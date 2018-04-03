from django.urls import path
from django.views.generic import TemplateView
from .import views
from .views import *

app_name = 'landing'

urlpatterns = [
    # path('', views.main_page, name='main_page'),
    path('', TemplateView.as_view(template_name='landing/main.html')),
    path('landing_torneo/', views.verTorneos,name='verTorneos'),
    path('organizadores/', views.ver_organizadores, name='ver_organizadores' ),
    path('equipos/', views.ver_equipos, name='ver_equipos'),
    path('equipo/<int:pk>', views.detalle_equipo, name='detalle_equipo'),
    path('torneos/', views.ver_torneos, name='ver_torneos'),
    path('torneos/<int:pk>', views.detalle_torneo, name='detalle_torneo'),
    path('torneos/<int:id_torneo>/partido/<slug:id_partido>', views.detalle_partido, name='detalle_partido'),

]
