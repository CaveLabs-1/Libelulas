from django.shortcuts import render
from .forms import jugadoraForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from jugadora.models import Jugadora
from equipo.models import Equipo
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

# Create your views here.


def agregar_jugadora(request, equipo_id=''):
    lista_equipo = ''

    if equipo_id != '':
        lista_equipo = Equipo.objects.get(id=equipo_id)

    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES)
        if form.is_valid():
            jugadora = form
            e = Equipo.objects.get(id=(request.POST['equipo']))
            e.jugadoras.add(jugadora.save())
            e.save()
            messages.success(request, 'Jugadora agregada exitosamente')
            return HttpResponseRedirect(reverse('jugadora:agregar_jugadora'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = jugadoraForm()

    return render(request, 'jugadora/agregar_jugadora.html', {'form': form, 'lista_equipo':lista_equipo, 'equipo':equipo_id})

def editar_jugadora(request, jugadora_id):
    instance = get_object_or_404(Jugadora, id=jugadora_id)
    idEquipo = Jugadora.objects.get(id=jugadora_id).equipo_set.all().first().pk
    form = jugadoraForm(request.POST or None, instance=instance, initial={'equipo': idEquipo})


    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            jugadora = form
            if idEquipo != request.POST['equipo']:
                re = Equipo.objects.get(id=idEquipo)
                re.jugadoras.remove(Jugadora.objects.get(id=jugadora_id))
                re.save()

                e = Equipo.objects.get(id=(request.POST['equipo']))
                e.jugadoras.add(jugadora.save())
                e.save()
            else:
                jugadora.save()
            messages.success(request, 'Jugadora editada exitosamente')
            return HttpResponseRedirect(reverse('jugadora:agregar_jugadora'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'jugadora/editar_jugadora.html', {'form': form, 'jugadora': instance })

def ver_jugadoras(request):
    jugadoras = Jugadora.objects.all()
    return render(request, 'jugadora/ver_jugadoras.html', {'jugadoras': jugadoras})

class eliminar_jugadora(DeleteView):
    model = Jugadora
    success_url = reverse_lazy('jugadora:ver_jugadoras')

