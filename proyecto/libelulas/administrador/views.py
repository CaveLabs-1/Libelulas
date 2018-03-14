from django.shortcuts import render, get_object_or_404
from .forms import UserForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User

def lista_administrador(request):
    lista = User.objects.all()
    return render(request, 'lista_administrador.html', {'lista': lista})

def agregar_administrador(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            informacion = form.save(commit=False)
            administrador = User()
            administrador.first_name = informacion.first_name
            administrador.username = informacion.username
            administrador.email = informacion.email
            administrador.password = informacion.password
            administrador.save()
            messages.success(request, 'Administrador agregado exitosamente')
            return HttpResponseRedirect(reverse('administrador:editar_administrador', kwargs={'id_administrador':administrador.id}))
    else:
        form = UserForm()
    return render(request, 'agregar_administrador.html', {'form': form})

def editar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    if request.method == "POST":
        form = UserForm(data=request.POST, instance=administrador)
        if form.is_valid():
            actualizar = form.save(commit=False)
            administrador.first_name = actualizar.first_name
            administrador.username = actualizar.username
            administrador.email = actualizar.email
            administrador.password = actualizar.password
            administrador.save()
            messages.success(request, 'Administrador editado exitosamente')
            url = reverse('administrador:editar_administrador', kwargs={'id_administrador':id_administrador})
            return HttpResponseRedirect(url)
    else:
        form = UserForm()
    return render(request, 'editar_administrador.html', {'form': form, 'administrador': administrador})

def eliminar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    administrador.delete()
    messages.warning(request, 'Administrador eliminado exitosamente.')
    return HttpResponseRedirect(reverse('administrador:lista_administrador'))

