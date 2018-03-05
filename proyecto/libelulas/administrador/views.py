from django.shortcuts import render
from .forms import UserForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

def agregar_administrador(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrador agregado exitosamente')
            return HttpResponseRedirect(reverse('administrador:agregar_administrador'))
    else:
        form = UserForm()

    return render(request, 'agregar_administrador.html', {'form': form})

