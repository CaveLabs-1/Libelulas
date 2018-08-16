from django.template.loader import render_to_string
from django.shortcuts import render
from equipo.models import Equipo
from jugadora.models import Jugadora
from equipo.models import Equipo
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Count
from torneo.models import *
from django.http import *
import datetime
from datetime import date



from torneo.models import Torneo



#Visualiza lista de torneos
def verTorneos (request):
    torneos= Torneo.objects.filter(activo=True)
    return render(request,'landing/torneos.html',{'torneos':torneos})

#Visualizar organizadores
def ver_organizadores(request):
    return render(request, 'landing/organizadores.html')

#Visualizar lista de equipos
def ver_equipos(request):
    equipos = Equipo.objects.all().filter(activo=True)
    return render(request, 'landing/lista_equipos.html', {'equipos': equipos})

#Visualizar sección social
def social(request):
    return render(request, 'landing/social.html')

#Visualizar galeria
def galeria(request):
    return render(request, 'landing/galeria.html')

#Visualizar detalles y estadísticas de los equipos
def detalle_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    jugadoras_equipo = Equipo.objects.get(id=pk).jugadoras.all()
    top_goles = Goles.objects.values('jugadora__nombre', 'jugadora__id', 'jugadora__apellido', 'jugadora__imagen').filter(jugadora__equipo=pk).annotate(goles=Sum('cantidad')).order_by('-goles')[:3]
    top_tarjetas_azules = Tarjetas_azules.objects.values('jugadora__nombre', 'jugadora__id', 'jugadora__apellido', 'jugadora__imagen', 'jugadora_id').filter(jugadora__equipo=pk).annotate(ta=Count('jugadora_id')).order_by('-ta')[:3]
    top_tarjetas_amarillas = TarjetasAmarillas.objects.values('jugadora__nombre', 'jugadora__id', 'jugadora__apellido', 'jugadora__imagen').filter(jugadora__equipo=pk).annotate(tam=Sum('cantidad')).order_by('-tam')[:3]
    top_tarjetas_rojas = TarjetasRojas.objects.values('jugadora__nombre', 'jugadora__id', 'jugadora__apellido', 'jugadora__imagen', 'jugadora_id').filter(jugadora__equipo=pk).annotate(tr=Count('jugadora_id')).order_by('-tr')[:3]
    torneos_ganados = Estadisticas.objects.all().filter(ganador=True).filter(equipo=pk).values('torneo__nombre', 'torneo__fecha_inicio')
    return render (request, 'landing/detalle_equipo.html', {
                                                            'equipo': equipo,
                                                            'jugadoras_equipo': jugadoras_equipo,
                                                            'top_goles': top_goles,
                                                            'top_tarjetas_azules': top_tarjetas_azules,
                                                            'top_tarjetas_amarillas': top_tarjetas_amarillas,
                                                            'top_tarjetas_rojas': top_tarjetas_rojas,
                                                            'torneos_ganados': torneos_ganados,
                                                            })

#Visualizar detalles y estadísticas de las jugadoras
def detalle_jugadora(request, id_equipo, id_jugadora):
    jugadora = get_object_or_404(Jugadora, pk=id_jugadora)
    today = date.today()
    equipo = Equipo.objects.get(id=id_equipo)
    edad = today.year - jugadora.nacimiento.year - ((today.month, today.day) < (jugadora.nacimiento.month, jugadora.nacimiento.day))
    asistencia = Asistencia.objects.filter(jugadora_id=id_jugadora).filter(equipo_id=id_equipo).count()
    asistencia_equipo = Asistencia.objects.filter(equipo_id=id_equipo).count()
    if(asistencia == 0):
        asistenciaE = 0
    else:
        asistenciaE = asistencia/ asistencia_equipo
    goles = Goles.objects.filter(jugadora_id=id_jugadora).filter(equipo_id=id_equipo).aggregate(Sum('cantidad'))['cantidad__sum']
    goles_equipo = Goles.objects.filter(equipo_id=id_equipo).aggregate(Sum('cantidad'))['cantidad__sum']
    if(goles == None):
        golesE = 0
    else:
        golesE = goles/goles_equipo
    tarjetas_rojas = TarjetasRojas.objects.filter(jugadora_id=id_jugadora).filter(jugadora__equipo=id_equipo).count()
    tarjetas_amarillas = TarjetasAmarillas.objects.filter(jugadora_id=id_jugadora).filter(jugadora__equipo=id_equipo).aggregate(Sum('cantidad'))['cantidad__sum']
    tarjetas_azul = Tarjetas_azules.objects.filter(jugadora_id=id_jugadora).filter(jugadora__equipo=id_equipo).count()
    return render(request, 'landing/detalle_jugadora.html', {
                                                                'jugadora': jugadora,
                                                                'equipo': equipo,
                                                                'edad': edad,
                                                                'asistencia': asistencia,
                                                                'asistencia_equipo': asistencia_equipo,
                                                                'asistenciaE': asistenciaE,
                                                                'goles': goles,
                                                                'goles_equipo': goles_equipo,
                                                                'golesE': golesE,
                                                                'tarjetas_rojas': tarjetas_rojas,
                                                                'tarjetas_amarillas': tarjetas_amarillas,
                                                                'tarjetas_azul': tarjetas_azul,
                                                            })

#Visualizar detalles y estadísticas de los partidos
def detalle_partido(request, id_torneo, id_partido):
    torneo = get_object_or_404(Torneo, pk=id_torneo)
    partido = get_object_or_404(Partido, pk=id_partido)
    equipo_local = get_object_or_404(Equipo, pk=partido.equipo_local_id)
    equipo_visitante = get_object_or_404(Equipo, pk=partido.equipo_visitante_id)
    asistencia = Asistencia.objects.filter(partido_id=id_partido).values('jugadora_id')
    jugadoras_local = Jugadora.objects.filter(id__in=asistencia).filter(equipo=partido.equipo_local_id)
    jugadoras_visitante = Jugadora.objects.filter(id__in=asistencia).filter(equipo=partido.equipo_visitante_id)
    tarjetas_rojas_local = TarjetasRojas.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_local_id)
    tarjetas_rojas_visitante = TarjetasRojas.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_visitante_id)
    tarjetas_amarillas_local = TarjetasAmarillas.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_local_id)
    tarjetas_amarillas_visitante = TarjetasAmarillas.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_visitante_id)
    goles_local = Goles.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_local_id)
    goles_visitante = Goles.objects.all().filter(partido=id_partido).filter(equipo=partido.equipo_visitante_id)
    tarjetas_azul_local = Tarjetas_azules.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_local_id)
    tarjetas_azul_visitante = Tarjetas_azules.objects.filter(partido=id_partido).filter(jugadora__equipo=partido.equipo_visitante_id)
    return render(request, 'landing/partido.html', {
                                                    'torneo' : torneo,
                                                    'partido' : partido,
                                                    'equipo_local': equipo_local,
                                                    'equipo_visitante': equipo_visitante,
                                                    'jugadoras_local' : jugadoras_local,
                                                    'jugadoras_visitante': jugadoras_visitante,
                                                    'tarjetas_rojas_local': tarjetas_rojas_local,
                                                    'tarjetas_rojas_visitante': tarjetas_rojas_visitante,
                                                    'tarjetas_amarillas_local': tarjetas_amarillas_local,
                                                    'tarjetas_amarillas_visitante': tarjetas_amarillas_visitante,
                                                    'goles_local': goles_local,
                                                    'goles_visitante': goles_visitante,
                                                    'tarjetas_azul_local': tarjetas_azul_local,
                                                    'tarjetas_azul_visitante': tarjetas_azul_visitante})

#Visualizar lista de torneos
def ver_torneos(request):
    torneos = Torneo.objects.all().order_by("-fecha_inicio")
    return render(request, 'landing/lista_torneos.html', {'torneos': torneos})

#Visualizar detalles y estadísticas de los torneos
def detalle_torneo(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    jornadas = Jornada.objects.filter(torneo=torneo)
    weones=[]
    for equipo in torneo.equipos.all():
        stats=Estadisticas.objects.filter(torneo=torneo).filter(equipo=equipo).first()
        jj=stats.jugados
        jg=stats.ganados
        jp=stats.perdidos
        je=stats.empatados
        pts=stats.puntos
        gf=stats.goles_favor
        ge=stats.goles_contra
        dg=gf-ge
        win=stats.ganador
        weones.append({'equipo':equipo, 'jj':jj, 'jg':jg,'jp':jp,'je':je,'gf':gf,'ge':ge,'dg':dg,'pts':pts, 'win':win})
    newlist = sorted(weones, key=lambda k: k['pts'], reverse=True)
    try:
        golit = Goles.objects.filter(partido__jornada__torneo= torneo).values('jugadora__nombre', 'jugadora', 'jugadora__apellido', 'jugadora__imagen', 'jugadora__equipo' , 'jugadora__id').annotate(goles=Sum('cantidad')).order_by('-goles')[:3]
        tarjetasAma = TarjetasAmarillas.objects.filter(partido__jornada__torneo= torneo).values('jugadora__nombre', 'jugadora', 'jugadora__apellido', 'jugadora__imagen', 'jugadora__equipo', 'jugadora__id').annotate(total=Sum('cantidad')).order_by('-total')[:3]
        tarjetasR = TarjetasRojas.objects.filter(partido__jornada__torneo= torneo).values('jugadora__nombre', 'jugadora', 'jugadora__apellido', 'jugadora__imagen', 'jugadora__equipo', 'jugadora__id').annotate(total=Count('jugadora')).order_by('-total')[:3]
        tarjetasAzul = Tarjetas_azules.objects.filter(partido__jornada__torneo= torneo).values('jugadora__nombre', 'jugadora', 'jugadora__apellido', 'jugadora__imagen', 'jugadora__equipo', 'jugadora__id').annotate(total=Count('jugadora')).order_by('-total')[:3]
        golEquipos = Goles.objects.filter(partido__jornada__torneo=torneo).values('equipo__nombre', 'equipo__logo', 'equipo__id').annotate(goles=Sum('cantidad')).order_by('-goles')[:3]
        taEquipo = TarjetasAmarillas.objects.filter(partido__jornada__torneo=torneo).values('jugadora__equipo__nombre', 'jugadora__equipo__logo', 'jugadora__equipo__id').annotate(total=Sum('cantidad')).order_by('-total')[:3]
        tazEquipo = Tarjetas_azules.objects.filter(partido__jornada__torneo=torneo).values('jugadora__equipo__nombre', 'jugadora__equipo__logo', 'jugadora__equipo__id').annotate(total=Count('jugadora')).order_by('-total')[:3]
        trEquipo = TarjetasRojas.objects.filter(partido__jornada__torneo=torneo).values('jugadora__equipo__nombre', 'jugadora__equipo__logo', 'jugadora__equipo__id').annotate(total=Count('jugadora')).order_by('-total')[:3]
    except:
        golit = None
        tarjetasAma = None
        tarjetasR = None
        tarjetasAzul = None
        golEquipos = None
        taEquipo = None
        tazEquipo = None
        trEquipo = None
    return render (request, 'landing/detalle_torneo.html', {
                                                                'torneo': torneo,
                                                                'stats': newlist,
                                                                'jornadas': jornadas,
                                                                'goles': golit,
                                                                'amarillas':tarjetasAma,
                                                                'rojas': tarjetasR,
                                                                'azules': tarjetasAzul,
                                                                'golEquipos': golEquipos,
                                                                'taEquipo': taEquipo,
                                                                'tazEquipo': tazEquipo,
                                                                'trEquipo': trEquipo
                                                                })

#Visualizar lista de partidos
def carga_partidos(request):
    if request.method == 'POST':
        id_jornada= int(request.POST.get('jornada'))
        jornada = get_object_or_404(Jornada, id=id_jornada)
        partidos = Partido.objects.filter(jornada=jornada)
        html = render_to_string('landing/lista_partidos.html', {'partidos':partidos,'jornada':jornada, 'datetime':datetime.date.today()})
        return HttpResponse(html)

#Visualizar partidos en la landing page
def landing(request):
    start_date = datetime.date.today()
    end_date = start_date+ datetime.timedelta(366)
    t = Partido.objects.filter(fecha__range=(start_date, end_date)).order_by("fecha")[:3]
    return render(request, 'landing/main.html', {'partidos': t})
