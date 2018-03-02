from django.shortcuts import render
from .forms import jugadoraForm

# Create your views here.

def agregar_jugadora(request):
    if request.method == "POST":
        form = jugadoraForm(request.POST)
        if form.is_valid():
            jugadora = form.save()
            jugadora.save()
            print("hola")
            return reverse('agregar_jugadora')
        else:
            print("no valido")
    else:
            print("hola2")
            form = jugadoraForm()

    return render(request, 'jugadora/agregar_jugadora.html', {'form':form})
