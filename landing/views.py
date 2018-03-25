from django.shortcuts import render
from equipo.models import Equipo
from jugadora.models import Jugadora

# Create your views here.
def ver_organizadores(request):
    return render(request, 'landing/organizadores.html')

def ver_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'landing/lista_equipos.html', {'equipos': equipos})

def detalle_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, pk=equipo_id)
    jugadoras_equipo = Equipo.objects.get(id=equipo_id).jugadoras.all()
    return (request, 'landing/detalle_equipo.html', {'equipo': equipo, 'jugadoras_equipo': jugadoras_equipo})
