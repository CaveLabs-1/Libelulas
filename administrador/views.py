from django.shortcuts import render, get_object_or_404
from .forms import UserForm, UpdatePasswordForm, UpdateUserForm
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
            administrador.set_password('temporal')
            administrador.save()
            messages.success(request, 'Administrador agregado exitosamente')
            return HttpResponseRedirect(reverse('administrador:confirmar_contrasena', kwargs={'id_administrador':administrador.id}))
    else:
        form = UserForm()
    return render(request, 'agregar_administrador.html', {'form': form})

def confirmar_contrasena(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    if request.method == "POST":
        form = UpdatePasswordForm(data=request.POST, instance=request.user)
        if form.is_valid():
            actualizar = form.save(commit=False)
            administrador.set_password(actualizar.password)
            administrador.save()
            messages.success(request, 'Contraseña actualizada exitosamente.')
            url = reverse('administrador:editar_administrador', kwargs={'id_administrador':id_administrador})
            return HttpResponseRedirect(url)
    else:
        form = UpdatePasswordForm()
    return render(request, 'confirmar_contrasena.html', {'form': form, 'administrador': administrador})

def editar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    if request.method == "POST":
        form = UpdateUserForm(data=request.POST, instance=administrador)
        if form.is_valid():
            actualizar = form.save(commit=False)
            administrador.first_name = actualizar.first_name
            administrador.email = actualizar.email
            administrador.save()
            messages.success(request, 'Administrador editado exitosamente')
            url = reverse('administrador:editar_administrador', kwargs={'id_administrador':id_administrador})
            return HttpResponseRedirect(url)
    else:
        form = UpdateUserForm(instance=administrador)
    return render(request, 'editar_administrador.html', {'form': form, 'administrador': administrador})

def eliminar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    administrador.delete()
    messages.warning(request, 'Administrador eliminado exitosamente.')
    return HttpResponseRedirect(reverse('administrador:lista_administrador'))

