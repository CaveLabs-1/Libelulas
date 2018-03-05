from django.shortcuts import render

# Create your views here.
from .forms import equipoForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.


def agregar_equipo(request):
    if request.method == "POST":
        form = equipoForm(request.POST, request.FILES)
        if form.is_valid():
            equipo = form.save()
            equipo.save()
            messages.success(request, 'Equipo creado exitosamente')
            return HttpResponseRedirect(reverse('equipo:agregar_equipo'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = equipoForm()

    return render(request, 'equipo/agregar_equipo.html', {'form': form})
