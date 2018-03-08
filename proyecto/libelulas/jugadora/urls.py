from django.urls import path
from .import views

app_name = 'jugadora'

urlpatterns = [
    path('agregar_jugadora/', views.agregar_jugadora, name='agregar_jugadora'),
    path('editar/<int:jugadora_id>', views.editar_jugadora, name='editar_jugadora'),
]
