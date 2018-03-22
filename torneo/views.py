from django.shortcuts import render
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from torneo.models import Torneo, Partido
from equipo.models import Equipo
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

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

def registrar_partido(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    equipo_local = Equipo.objects.get(id=partido.equipo_local)
    equipo_visitante = Equipo.objects.get(id=partido.equipo_visitante)
    form_partido = PartidoForm(instance=cedula)
    form_tarjeta_amarilla = TarjetaAmarillaForm()
    form_tarjeta_roja = TarjetaRojaForm()
    form_tarjeta_azul = TarjetaAzulForm()
    if request.method == 'POST':
        if form.is_valid():
            return True
    return render(request, 'torneo/registrar_partido.html', {'form':form, 'data':data})
