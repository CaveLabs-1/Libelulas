from django.shortcuts import render
from .forms import torneoForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from torneo.models import *
from equipo.models import Equipo
from django.views.generic.list import ListView
from torneo.models import Torneo
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from django.conf import settings

def lista_torneos(request):

    lista_torneos = Torneo.objects.all()
    return render(request, 'torneo/torneo_list.html', {'lista_torneos': lista_torneos})

def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    return render(request, 'torneo/torneo_detail.html', {'torneo': torneo, 'equipos':torneo.equipos.all})

def crear_torneo(request):
    lista_equipo = Equipo.objects.all()

    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES)
        if form.is_valid():
            torneo = form
            torneo.save()
            messages.success(request, 'Torneo agregado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
            form = torneoForm()

    return render(request, 'torneo/agregar_torneo.html', {'form': form, 'lista_equipo':lista_equipo})

def editar_torneo(request, torneo_id):
    instance = get_object_or_404(Torneo, id=torneo_id)
    form = torneoForm(instance=instance)
    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            torneo = form
            torneo.save()
            messages.success(request, 'Torneo editado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'torneo/torneo_editar.html', {'form': form, 'torneo':instance})


class eliminar_torneo(DeleteView):
    model = Torneo
    success_url = reverse_lazy('torneo:lista_torneos')

def eliminar_equipo(request, id_equipo, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    equipo = get_object_or_404(Equipo, id=id_equipo)
    if equipo in torneo.equipos.all():
        torneo.equipos.remove(equipo)
        messages.success(request, 'Equipo eliminado exitosamente')
        return HttpResponseRedirect(reverse('torneo:detalle_torneo',kwargs={'torneo_id':id_torneo}))


def cerrar_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    if torneo.activo:
        torneo.activo = False
        torneo.save()
        numero_equipos = len(torneo.equipos.all())
        numero_jornadas = (numero_equipos - 1) * 2
        fecha_inicial = torneo.fechaInicio
        fecha_fin =  fecha_inicial + timezone.timedelta(days=6)

        for i in range(numero_jornadas):
            descripcion = "Jornada "+str(i+1)
            jornada = Jornada(jornada=descripcion,torneo=torneo,fecha_inicio=fecha_inicial,fecha_fin=fecha_fin)
            fecha_inicial = fecha_fin + timezone.timedelta(days=1)
            fecha_fin =  fecha_inicial + timezone.timedelta(days=6)
            jornada.save()
        jornadas = Jornada.objects.filter(torneo=torneo)
        equipos = Equipo.objects.filter(torneo=torneo)
        lista = []
        for equipo in equipos:
            lista.append(equipo)
        print(lista)
        for i,jornada in enumerate(jornadas):
            s = []
            if numero_equipos % 2 == 1: lista = lista + ["BYE"]
            mid = len(lista) / 2
            l1 = equipos[:mid]
            l2 = equipos[mid:]
            l2.reverse()
            if(i % 2 == 1):
                s = s + [ zip(l1, l2) ]
            else:
                s = s + [ zip(l2, l1) ]

                lista.insert(1, lista.pop())

            print(s)
            # dias_adelante = equipo_local.dia - jornada.fecha_inicio.weekday()
            # if dias_adelante <= 0:
            #     dias_adelante += 7
            #     fecha =  jornada.fecha_inicio + datetime.timedelta(dias_adelante)
            #
            # partido = Partido(jornada=jornada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, fecha=fecha,hora=equipo_local.hora,cancha=equipo_local.cancha)
            # partido.save()
        return HttpResponseRedirect(reverse('torneo:lista_torneos'))

def mandar_codigoCedula(request, torneo_id, jornada_id):

    torneos = get_object_or_404(Torneo, id=torneo_id)

    jornadas = get_object_or_404(torneos.jornada_set.all(), id=jornada_id)

    partidos = jornadas.partido_set.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Partidos.pdf"'




    buffer = BytesIO()
    p = canvas.Canvas(buffer)


    # Start writing the PDF here
    posX = 0
    posY = 830
    posX += 250
    posY -= 50
    p.drawString(posX, posY, 'Lista de Partidos')
    posY -= 20
    p.drawString(posX, posY, torneos.nombre)
    p.drawString(50, 740, 'Jornada: '+jornadas.jornada)
    p.drawString(100, 720, 'Fecha de Inicio: '+str(jornadas.fecha_inicio.strftime("%d-%B-%Y")))
    p.drawString(100, 700, 'Fecha Final: '+str(jornadas.fecha_inicio.strftime("%d-%B-%Y")))
    p.drawString(50, 650, 'Partidos')
    posX=75
    posY=650

    for partido in partidos:

        if posY <= 50:
            p.showPage()
            posY=800

        posY-=15

        p.drawString(posX, posY, str(partido.equipo_local.nombre)+" vs "+partido.equipo_visitante.nombre)
        posY-=15
        p.drawString(100, posY, "Fecha del Partido: "+partido.fecha.strftime("%d-%B-%Y"))
        posY -= 15
        p.drawString(100, posY, "Hora del Partido: " + partido.hora.strftime("%H:%M"))
        posY -= 15
        p.drawString(100, posY, "Codido de acceso a la cedula del partido: " + partido.id)
        posY-=10
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
    #return HttpResponseRedirect(reverse('torneo:lista_torneos'))
