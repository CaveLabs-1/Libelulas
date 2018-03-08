from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from .forms import equipoForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

from django.views.generic.list import ListView
from .models import Equipo
from jugadora.models import Jugadora

from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView


def agregar_equipo(request):
    if request.method == "POST":
        form = equipoForm(request.POST, request.FILES)
        if form.is_valid():
            equipo = form.save()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class detalle_equipo(DetailView):

    model = Equipo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView

class editar_equipo(UpdateView):
    model = Equipo
    fields = ['nombre', 'representante', 'telefono', 'correo', 'logo', 'colorLocal', 'colorVisitante', 'cancha', 'dia', 'hora']
    template_name_suffix = '_update'
    success_url = reverse_lazy('equipo:lista_equipos')

from django.urls import reverse_lazy

class borrar_equipo(DeleteView):
    model = Equipo
    success_url = reverse_lazy('equipo:lista_equipos')


