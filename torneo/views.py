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
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy



def lista_torneos(request):
    lista_torneos=Torneo.objects.all()
    return render(request, 'torneo/torneo_list.html', { 'lista_torneos':lista_torneos})

from django.views.generic.detail import DetailView

from .models import Torneo

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
