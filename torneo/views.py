from django.shortcuts import render
from .forms import torneoForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from torneo.models import *
from equipo.models import Equipo
from django.views.generic.list import ListView
from torneo.models import Torneo
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
import datetime

def lista_torneos(request):

    lista_torneos = Torneo.objects.all()
    return render(request, 'torneo/torneo_list.html', {'lista_torneos': lista_torneos})

def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    return render(request, 'torneo/torneo_detail.html', {'torneo': torneo, 'equipos':torneo.equipos.all})

def crear_torneo(request):
    lista_equipo = Equipo.objects.all()

    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES)
        if form.is_valid():
            torneo = form
            torneo.save()
            messages.success(request, 'Torneo agregado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = torneoForm()

    return render(request, 'torneo/agregar_torneo.html', {'form': form, 'lista_equipo':lista_equipo})

def editar_torneo(request, torneo_id):
    instance = get_object_or_404(Torneo, id=torneo_id)
    form = torneoForm(instance=instance)
    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            torneo = form
            torneo.save()
            messages.success(request, 'Torneo editado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'torneo/torneo_editar.html', {'form': form, 'torneo':instance})


class eliminar_torneo(DeleteView):
    model = Torneo
    success_url = reverse_lazy('torneo:lista_torneos')

def eliminar_equipo(request, id_equipo, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    equipo = get_object_or_404(Equipo, id=id_equipo)
    if equipo in torneo.equipos.all():
        torneo.equipos.remove(equipo)
        messages.success(request, 'Equipo eliminado exitosamente')
        return HttpResponseRedirect(reverse('torneo:detalle_torneo',kwargs={'torneo_id':id_torneo}))


def cerrar_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    if torneo.activo:
        torneo.activo = False
        torneo.save()
        numero_equipos = len(torneo.equipos.all())
        numero_jornadas = (numero_equipos - 1) * 2
        fecha_inicial = torneo.fechaInicio
        fecha_fin =  fecha_inicial + timezone.timedelta(days=6)

        for i in range(numero_jornadas):
            descripcion = "Jornada "+str(i+1)
            jornada = Jornada(jornada=descripcion,torneo=torneo,fecha_inicio=fecha_inicial,fecha_fin=fecha_fin)
            fecha_inicial = fecha_fin + timezone.timedelta(days=1)
            fecha_fin =  fecha_inicial + timezone.timedelta(days=6)
            jornada.save()
        jornadas = Jornada.objects.filter(torneo=torneo)
        for jornada in jornadas[:(numero_jornadas/2)]:
            for equipo_local in torneo.equipos.all():
                for equipo_visitante in torneo.equipos.all():
                    if equipo_local is not equipo_visitante:
                        dias_adelante = equipo_local.dia - jornada.fecha_inicio.weekday()
                        if dias_adelante <= 0:
                            dias_adelante += 7
                            fecha =  jornada.fecha_inicio + datetime.timedelta(dias_adelante)
                        partido = Partido(jornada=jornada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, fecha=fecha,hora=equipo_local.hora,cancha=equipo_local.cancha)
                        partido.save()

        for jornada in reversed(jornadas[:(numero_jornadas/2)]):
            for equipo_local in torneo.equipos.all():
                for equipo_visitante in torneo.equipos.all():
                    if equipo_local is not equipo_visitante:
                        dias_adelante = equipo_visitante.dia - jornada.fecha_inicio.weekday()
                        if dias_adelante <= 0:
                            dias_adelante += 7
                            fecha =  jornada.fecha_inicio + datetime.timedelta(dias_adelante)
                        partido = Partido(jornada=jornada, equipo_local=equipo_visitante, equipo_visitante=equipo_local, fecha=fecha,hora=equipo_visitante.hora,cancha=equipo_visitante.cancha)
                        partido.save()
        return HttpResponseRedirect(reverse('torneo:lista_torneos'))
