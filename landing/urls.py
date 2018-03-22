from django.urls import path
from django.views.generic import TemplateView
from .import views

app_name = 'landing'

urlpatterns = [
    # path('', views.main_page, name='main_page'),
    path('', TemplateView.as_view(template_name='landing/main.html')),
    path('organizadores/', views.ver_organizadores, name='ver_organizadores' ),
]
