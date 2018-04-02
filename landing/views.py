
from django.shortcuts import render

# Create your views here.

from torneo.models import Torneo


# Create your views here.

def verTorneos (request):
    torneos= Torneo.objects.filter(activo=True)
    return render(request,'landing/torneos.html',{'torneos':torneos})
