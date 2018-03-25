from django.shortcuts import render
from equipo.models import Equipo
from jugadora.models import Jugadora
from django.shortcuts import get_object_or_404

# Create your views here.
def ver_organizadores(request):
    return render(request, 'landing/organizadores.html')

def ver_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'landing/lista_equipos.html', {'equipos': equipos})

def detalle_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    jugadoras_equipo = Equipo.objects.get(id=pk).jugadoras.all()
    return render (request, 'landing/detalle_equipo.html', {'equipo': equipo, 'jugadoras_equipo': jugadoras_equipo})
