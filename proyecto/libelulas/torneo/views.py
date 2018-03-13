from django.shortcuts import render
from .forms import torneoForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from torneo.models import Torneo
from equipo.models import Equipo
from django.views.generic.list import ListView
from torneo.models import Torneo


def lista_torneos(request):
    lista_torneos=Torneo.objects.all()
    return render(request, 'torneo/torneo_list.html', { 'lista_torneos':lista_torneos})

from django.views.generic.detail import DetailView

from .models import Torneo

def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    return render(request, 'torneo/torneo_detail.html', {'torneo': torneo, 'equipos':torneo.equipos.all})



def crear_torneo(request):

    #lista_equipo = ''

    #if equipo_id != '':
     #   lista_equipo = Equipo.objects.get(id=equipo_id)

    lista_equipo = Equipo.objects.all()

    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES)
        if form.is_valid():
            torneo = form
            #print (request.POST['equipos'])
            #torneo.equipos.add(request.POST['equipos'])
            torneo.save()
            messages.success(request, 'Torneo agregado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = torneoForm()

    return render(request, 'torneo/agregar_torneo.html', {'form': form, 'lista_equipo':lista_equipo})

