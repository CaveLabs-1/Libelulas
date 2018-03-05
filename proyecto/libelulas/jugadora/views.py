from django.shortcuts import render
from .forms import jugadoraForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.


def agregar_jugadora(request):
    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES)
        if form.is_valid():
            jugadora = form.save()
            jugadora.save()
            messages.success(request, 'Jugadora agregada exitosamente')
            return HttpResponseRedirect(reverse('jugadora:agregar_jugadora'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = jugadoraForm()

    return render(request, 'jugadora/agregar_jugadora.html', {'form': form})
