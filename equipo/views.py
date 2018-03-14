from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from .forms import equipoForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.

from django.views.generic.list import ListView
from .models import Equipo

from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView


from django.urls import reverse_lazy
from jugadora.models import Jugadora

def agregar_equipo(request):
    if request.method == "POST":
        form = equipoForm(request.POST, request.FILES)
        if form.is_valid():
            equipo = form
            equipo.save()
            messages.success(request, 'Equipo creado exitosamente')
            return HttpResponseRedirect(reverse('equipo:lista_equipos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = equipoForm()

    return render(request, 'equipo/agregar_equipo.html', {'form': form})


class lista_equipos(ListView):

    model = Equipo
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def detalle_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo ,pk=equipo_id)
    jugadoras_equipo = Equipo.objects.get(id=equipo_id).jugadoras.all()
    return render(request, 'equipo/equipo_detail.html', {'equipo': equipo, 'jugadoras_equipo': jugadoras_equipo })

def editar_equipo(request, pk):
    instance = get_object_or_404(Equipo, id=pk)
    form = equipoForm(instance=instance)
    if request.method == "POST":
        form = equipoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            equipo = form
            equipo.save()
            messages.success(request, 'Equipo editado exitosamente')
            return HttpResponseRedirect(reverse('equipo:lista_equipos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'equipo/equipo_update.html', {'form': form, 'equipo' : instance})

class borrar_equipo(DeleteView):
    model = Equipo
    success_url = reverse_lazy('equipo:lista_equipos')

def eliminar_jugadora(request, equipo_id, idJugadora):
    j =  Jugadora.objects.get(id=idJugadora)
    Equipo.objects.get(id=equipo_id).jugadoras.remove(j)
    return HttpResponseRedirect(reverse_lazy('equipo:lista_equipos'))
