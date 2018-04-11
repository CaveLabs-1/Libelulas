from django.shortcuts import render, get_object_or_404
from .forms import PreForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PreRegistro
from torneo.models import *
from equipo.forms import equipoForm

def pre_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo,id=id_torneo)
    if request.method == "POST":
        form = PreForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.torneo = torneo
            registro.save()
            messages.success(request, 'Solicitud de pre-registro enviada')
            return HttpResponseRedirect(reverse('coaches:pre_registro', kwargs={'id_torneo':id_torneo}))
    else:
        form = PreForm()
    return render(request, 'coaches/pre_registro.html', {'form': form})

def registrar_jugadora(request, codigo):

    return

def registrar_equipo(request, codigo):
    registro = get_object_or_404(PreRegistro,codigo=codigo)
    if request.method == "POST":
        form = equipoForm(request.POST, request.FILES)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.activo = False
            equipo.save()
            registro.equipo = equipo
            registro.save()
            messages.success(request, 'Equipo creado exitosamente')
            return HttpResponseRedirect(reverse('coaches:registrar_equipo',kwargs={'codigo':codigo}))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = equipoForm()
    return render(request, 'equipo/agregar_equipo.html', {'form': form})
