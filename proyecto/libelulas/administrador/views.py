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
            form.save()
            messages.success(request, 'Administrador agregado exitosamente')
            return HttpResponseRedirect(reverse('administrador:lista_administrador'))
    else:
        form = UserForm()
    return render(request, 'agregar_administrador.html', {'form': form})

def editar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            actualizar = form.save(commit=False)
            administrador.first_name = actualizar.first_name
            administrador.username = actualizar.username
            administrador.email = actualizar.email
            administrador.password = actualizar.password
            administrador.save()
            messages.success(request, 'Administrador editado exitosamente')
            return HttpResponseRedirect(reverse('administrador:lista_administrador'))
    else:
        form = UserForm()
    return render(request, 'editar_administrador.html', {'form': form, 'administrador': administrador})

