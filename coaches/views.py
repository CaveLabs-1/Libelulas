from django.shortcuts import render, get_object_or_404
from .forms import PreForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PreRegistro
from torneo.models import *

def pre_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo,id=id_torneo)
    if request.method == "POST":
        form = PreForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.torneo = torneo
            registro.save()
            messages.success(request, 'Solicitud de pre-registro enviada')
            return HttpResponseRedirect(reverse('coaches:pre_registro', kwargs={'id_torneo':id_torneo}))
    else:
        form = PreForm()
    return render(request, 'coaches/pre_registro.html', {'form': form})
