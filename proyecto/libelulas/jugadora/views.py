from django.shortcuts import render
from .forms import jugadoraForm

# Create your views here.

def agregar_jugadora(request):
    if request.method == "POST":
        form = jugadoraForm(request.POST)
        if form.is_valid():
            jugadora = form.save()
            jugadora.save()
            return redirect('agregar_jugadora')
    else:
            form = jugadoraForm()

    return render(request, 'jugadora/agregar_jugadora.html', {'form':form})
