from django.shortcuts import render, get_object_or_404
from .forms import PreForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PreRegistro
from torneo.models import *
from equipo.models import *
from equipo.forms import equipoForm
from jugadora.forms import *

def pre_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo,id=id_torneo)
    if request.method == "POST":
        form = PreForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.torneo = torneo
            registro.save()
            return HttpResponseRedirect(reverse('landing:ver_equipos'))
    else:
        form = PreForm()
    return render(request, 'coaches/pre_registro.html', {'form': form, 'torneo': torneo})

def registrar_jugadora(request, codigo, id_equipo):
    lista_equipo = get_object_or_404(Equipo,id=id_equipo)
    registro = get_object_or_404(PreRegistro,codigo=codigo)
    if request.method == "POST":
        form = jugadoraEquipoForm(request.POST, request.FILES)
        if form.is_valid():
            jugadora = form.save(commit=False)
            jugadora.activo = False
            jugadora.save()
            e = Equipo.objects.get(id=id_equipo)
            e.jugadoras.add(jugadora)
            e.save()
            messages.success(request, 'Jugadora agregada exitosamente')
            return HttpResponseRedirect(reverse('coaches:registrar_jugadora', kwargs={'codigo':codigo,'id_equipo':id_equipo}))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
        form = jugadoraEquipoForm()
    return render(request, 'coaches/agregar_jugadora.html', {'form': form, 'lista_equipo':lista_equipo, 'equipo':id_equipo, 'codigo':codigo})

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
    return render(request, 'coaches/agregar_equipo.html', {'form': form})

def terminar_registro(request, codigo):
    registro = get_object_or_404(PreRegistro,codigo=codigo)
    registro.codigo = None
    registro.save()
    messages.success(request, 'La solicitud será procesada por el administrador')
    return HttpResponseRedirect(reverse('landing:ver_equipos'))
