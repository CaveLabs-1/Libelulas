from django.shortcuts import render

# Create your views here.
def ver_organizadores(request):
    return render(request, 'landing/organizadores.html')
