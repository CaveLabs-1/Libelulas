from django.urls import path
from .import views

app_name = 'jugadora'

urlpatterns = [
    path('agregar_jugadora/', views.agregar_jugadora, name='agregar_jugadora'),
    path('editar/<int:jugadora_id>', views.editar_jugadora, name='editar_jugadora'),
    path('agregar_jugadora/<int:equipo_id>', views.agregar_jugadora, name='agregar_jugadora'),
    path('ver_jugadoras/', views.ver_jugadoras, name='ver_jugadoras'),
    path('eliminar/<int:pk>', views.eliminar_jugadora.as_view(), name='eliminar_jugadora'),
    path('<int:pk>', views.detalle_jugadora, name='detalle_jugadora'),
]
