
from django.shortcuts import render
from equipo.models import Equipo
from jugadora.models import Jugadora
from torneo.models import Torneo
from torneo.models import Partido
from torneo.models import Tarjetas_amarillas
from torneo.models import Tarjetas_rojas
from torneo.models import Tarjetas_azules
from torneo.models import Goles
from torneo.models import Asistencia
from equipo.models import Equipo
from django.shortcuts import get_object_or_404

# Create your views here.

from torneo.models import Torneo


# Create your views here.

def verTorneos (request):
    torneos= Torneo.objects.filter(activo=True)
    return render(request,'landing/torneos.html',{'torneos':torneos})
  
def ver_organizadores(request):
    return render(request, 'landing/organizadores.html')

def ver_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'landing/lista_equipos.html', {'equipos': equipos})

def detalle_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    jugadoras_equipo = Equipo.objects.get(id=pk).jugadoras.all()
    return render (request, 'landing/detalle_equipo.html', {'equipo': equipo, 'jugadoras_equipo': jugadoras_equipo})

def detalle_partido(request, id_torneo, id_partido):
    torneo = get_object_or_404(Torneo, pk=id_torneo)
    partido = get_object_or_404(Partido, pk=id_partido)
    equipo_local = get_object_or_404(Equipo, pk=partido.equipo_local_id)
    equipo_visitante = get_object_or_404(Equipo, pk=partido.equipo_visitante_id)
    asistencia = Asistencia.objects.filter(partido_id=id_partido).values('jugadora_id')
    jugadoras_local = Jugadora.objects.filter(id__in=asistencia).filter(equipo=partido.equipo_local_id)
    jugadoras_visitante = Jugadora.objects.filter(id__in=asistencia).filter(equipo=partido.equipo_visitante_id)

    # jugadoras_local = Asistencia.objects.filter(partido_id=id_partido)
    return render(request, 'landing/partido.html', {
                                                    'torneo' : torneo,
                                                    'partido' : partido,
                                                    'equipo_local': equipo_local,
                                                    'equipo_visitante': equipo_visitante,
                                                    'jugadoras_local' : jugadoras_local,
                                                    'jugadoras_visitante': jugadoras_visitante,
                                                     })

def ver_torneos(request):
    torneos = Torneo.objects.all().order_by("-fechaInicio")
    return render(request, 'landing/lista_torneos.html', {'torneos': torneos})

def detalle_torneo(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    partidos = Partido.objects.filter(torneo=pk)
    if partidos.exists():
        weones=[]
        for equipo in torneo.equipos.all():
            jj=jg=jp=je=pts=gf=ge=dg=ta=tr=tz=0
            for partido in partidos.all():
                if (partido.equipo_local == equipo or partido.equipo_visitante == equipo):
                    jj=jj+1
                if (partido.equipo_local == equipo and partido.goles_local>partido.goles_visitante):
                    jg=jg+1
                    gf=gf+partido.goles_local
                    ge=ge+partido.goles_visitante
                if (partido.equipo_visitante == equipo and partido.goles_visitante>partido.goles_local):
                    jg=jg+1
                    ge=ge+partido.goles_local
                    gf=gf+partido.goles_visitante
                if (partido.equipo_local == equipo and partido.goles_local<partido.goles_visitante):
                    jp=jp+1
                    gf=gf+partido.goles_local
                    ge=ge+partido.goles_visitante
                if (partido.equipo_visitante == equipo and partido.goles_visitante<partido.goles_local):
                    jp=jp+1
                    ge=ge+partido.goles_local
                    gf=gf+partido.goles_visitante
            je=jj-jg-jp
            pts=(jg*3)+(je*1)
            dg=gf-ge
            weones.append({'equipo':equipo, 'jj':jj, 'jg':jg,'jp':jp,'je':je,'gf':gf,'ge':ge,'dg':dg,'pts':pts})
        newlist = sorted(weones, key=lambda k: (k['pts'],k['dg'],k['gf']), reverse=True) 
        return render (request, 'landing/detalle_torneo.html', {'torneo': torneo,'stats': newlist})
    jj=jg=jp=je=pts=gf=ge=dg=ta=tr=tz=0
    weones=[]
    for equipo in torneo.equipos.all():
        weones.append({'equipo':equipo, 'jj':jj, 'jg':jg,'jp':jp,'je':je,'gf':gf,'ge':ge,'dg':dg,'pts':pts})
    newlist = sorted(weones, key=lambda k: k['pts'], reverse=True)
    return render (request, 'landing/detalle_torneo.html', {'torneo': torneo,'stats': newlist})                                          
