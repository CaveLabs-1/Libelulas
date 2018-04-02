from django.shortcuts import render
from .forms import *
from django.urls import reverse
from django.http import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from torneo.models import *
from equipo.models import Equipo
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils import timezone
import datetime
import uuid
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse

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

def registrar_partido(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    equipo_local = Equipo.objects.get(id=partido.equipo_local)
    equipo_visitante = Equipo.objects.get(id=partido.equipo_visitante)
    form_partido = PartidoForm(instance=cedula)
    form_tarjeta_amarilla = TarjetaAmarillaForm()
    form_tarjeta_roja = TarjetaRojaForm()
    form_tarjeta_azul = TarjetaAzulForm()
    if request.method == 'POST':
        if form.is_valid():
            return True
    return render(request, 'torneo/registrar_partido.html', {'form':form, 'data':data})

def cerrar_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    if torneo.activo:
        torneo.activo = False
        torneo.save()
        fecha_inicial = torneo.fechaInicio
        fecha_fin =  fecha_inicial + timezone.timedelta(days=6)
        equipos = torneo.equipos.all()
        id_last_j = 1
        lista = []
        for equipo in equipos:
            lista.append(equipo.nombre)
        lista_vuelta = []
        for equipo in equipos:
            lista_vuelta.append(equipo.nombre)
        lista_vuelta = lista_vuelta[::-1]
        jornadas_local = create_schedule(lista)
        jornadas_visitante = create_schedule(lista_vuelta)
        id_last_j,fecha_inicial,fecha_fin = partidos(id_last_j,jornadas_local,fecha_inicial,fecha_fin,torneo)
        partidos(id_last_j,jornadas_visitante,fecha_inicial,fecha_fin,torneo)
        messages.success(request,'El registro del torneo ha sido cerrado')
        return HttpResponseRedirect(reverse('torneo:lista_torneos'))

def create_schedule(list):
    s = []
    if len(list) % 2 == 1: list = list + ["BYE"]
    for i in range(len(list)-1):
        mid = len(list) / 2
        l1 = list[:int(mid)]
        l2 = list[int(mid):]
        l2.reverse()
        if(i % 2 == 1):
            s = s + [ zip(l1, l2) ]
        else:
            s = s + [ zip(l2, l1) ]
        list.insert(1, list.pop())
    return s

def partidos(id_last_j,jornadas_local,fecha_inicial,fecha_fin,torneo):
    for i,semana in enumerate(jornadas_local):
        descripcion = "J"+str(id_last_j)
        jornada = Jornada(jornada=descripcion,torneo=torneo,fecha_inicio=fecha_inicial,fecha_fin=fecha_fin)
        fecha_inicial = fecha_fin + timezone.timedelta(days=1)
        fecha_fin =  fecha_inicial + timezone.timedelta(days=6)
        jornada.save()
        for equipo in semana:
            if equipo[0] is not "BYE" and equipo[1] is not "BYE":
                equipo_local = get_object_or_404(Equipo, nombre=equipo[0])
                equipo_visitante = get_object_or_404(Equipo, nombre=equipo[1])
                dias_adelante = equipo_local.dia - jornada.fecha_inicio.weekday()
                if dias_adelante <= 0:
                    dias_adelante += 7
                    fecha =  jornada.fecha_inicio + datetime.timedelta(dias_adelante)
                partido = Partido(id=uuid.uuid4().hex[:6].upper(), jornada=jornada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, fecha=fecha,hora=equipo_local.hora,cancha=equipo_local.cancha)
                partido.save()
        id_last_j = id_last_j + 1
    return id_last_j, fecha_inicial, fecha_fin

def editar_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    jornadas = Jornada.objects.filter(torneo=torneo)
    return render(request, 'torneo/editar_registro.html', {'jornadas':jornadas})

def carga_partidos(request):
    if request.method == 'POST':
        id_jornada= int(request.POST.get('jornada'))
        jornada = get_object_or_404(Jornada, id=id_jornada)
        partidos = Partido.objects.filter(jornada=jornada)
        html = render_to_string('torneo/lista_partidos.html', {'partidos':partidos,'jornada':jornada})
        return HttpResponse(html)

def editar_partido(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    form = PartidoForm(instance=partido)
    if request.method == "POST":
        form = PartidoForm(request.POST,instance=partido)
        objeto = form.save(commit=False)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partido editado exitosamente')
            return HttpResponseRedirect(reverse('torneo:editar_registro',kwargs={'id_torneo':partido.jornada.torneo.id}))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'torneo/editar_partido.html', {'form': form, 'partido':partido})

def mandar_codigoCedula(request, torneo_id, jornada_id):

    torneo=Torneo.objects.get(id=torneo_id)
    jornada=torneo.jornada_set.get(id=jornada_id)

    html_template = render_to_string('torneo/pdf_template.html', {'torneo':torneo,'jornada':jornada})
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response
