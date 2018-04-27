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



#Desplegar forma para agregar jugadora
def agregar_jugadora(request, equipo_id=''):
    lista_equipo = ''

    if equipo_id != '':
        lista_equipo = Equipo.objects.get(id=equipo_id)
    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES)
        if form.is_valid():
            jugadora = form
            if request.POST['equipo'] != '':
                e = Equipo.objects.get(id=(request.POST['equipo']))
                e.jugadoras.add(jugadora.save())
                e.save()
            else:
                jugadora.save()
            messages.success(request, 'Jugadora agregada exitosamente')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = jugadoraForm()
    return render(request, 'jugadora/agregar_jugadora.html', {'form': form, 'lista_equipo':lista_equipo, 'equipo':equipo_id})


#Desplegar forma para editar jugadora
def editar_jugadora(request, jugadora_id):
    instance = get_object_or_404(Jugadora, id=jugadora_id)
    try:
        idEquipo = Jugadora.objects.get(id=jugadora_id).equipo_set.all().first().pk
    except Exception as e:
        idEquipo = ''
    form = jugadoraForm(request.POST or None, instance=instance, initial={'equipo': idEquipo})
    if request.method == "POST":
        form = jugadoraForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            jugadora = form
            if idEquipo != request.POST['equipo']:
                if idEquipo != '':
                    re = Equipo.objects.get(id=idEquipo)
                    re.jugadoras.remove(Jugadora.objects.get(id=jugadora_id))
                    re.save()
                if request.POST['equipo'] != "":
                    e = Equipo.objects.get(id=(request.POST['equipo']))
                    e.jugadoras.add(jugadora.save())
                    e.save()
            else:
                jugadora.save()
            messages.success(request, 'Jugadora editada exitosamente')
            return HttpResponseRedirect(reverse('jugadora:ver_jugadoras'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'jugadora/editar_jugadora.html', {'form': form, 'jugadora': instance })


#Desplegar lista de jugadoras activas
def ver_jugadoras(request):
    jugadoras = Jugadora.objects.filter(activo=True)
    return render(request, 'jugadora/ver_jugadoras.html', {'jugadoras': jugadoras})


#Eliminar una jugadora
class eliminar_jugadora(DeleteView):
    model = Jugadora

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Jugadora eliminada exitosamente')
        return super(eliminar_jugadora, self).delete(request, *args, **kwargs)
    success_url = reverse_lazy('jugadora:ver_jugadoras')
    warning_message = "Jugadora eliminada exitosamente"

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.warning_message)
        return super(eliminar_jugadora, self).delete(request, *args, **kwargs)


#Desplegar detalles de una jugadora
def detalle_jugadora(request, pk):
    jugadora = get_object_or_404(Jugadora, pk=pk)
    EquipoNombre = 'No pertenece a ningún equipo'
    Equipo = jugadora.equipo_set.all().first()
    if Equipo is not None:
        EquipoNombre = Equipo.nombre
    return render(request, 'jugadora/jugadora_detail.html', {'jugadora': jugadora, 'EquipoNombre':EquipoNombre})
