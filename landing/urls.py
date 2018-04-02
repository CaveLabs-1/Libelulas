from django.urls import path
from django.views.generic import TemplateView
from .import views
from .views import *

app_name = 'landing'

urlpatterns = [
    # path('', views.main_page, name='main_page'),
    path('', TemplateView.as_view(template_name='landing/main.html')),
    path('landing_torneo/', views.verTorneos,name='verTorneos'),

]
