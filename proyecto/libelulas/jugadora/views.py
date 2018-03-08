from django.shortcuts import render
from .forms import jugadoraForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from jugadora.models import Jugadora

# Create your views here.


def agregar_jugadora(request):
    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES)
        if form.is_valid():
            jugadora = form
            jugadora.save()
            messages.success(request, 'Jugadora agregada exitosamente')
            return HttpResponseRedirect(reverse('jugadora:agregar_jugadora'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = jugadoraForm()

    return render(request, 'jugadora/agregar_jugadora.html', {'form': form})

def editar_jugadora(request, jugadora_id):
    instance = get_object_or_404(Jugadora, id=jugadora_id)
    form = jugadoraForm(request.POST or None, instance=instance)
    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            jugadora = form
            jugadora.save()
            messages.success(request, 'Jugadora editada exitosamente')
            return HttpResponseRedirect(reverse('jugadora:agregar_jugadora'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'jugadora/editar_jugadora.html', {'form': form, 'jugadora' : instance})
