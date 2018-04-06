from django.shortcuts import render
from .forms import *
from django.urls import reverse
from django.http import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from torneo.models import *
from equipo.models import Equipo
from jugadora.models import Jugadora
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Sum, Count
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
            torneo = form.save(commit=False)
            torneo.save()
            for equipo in form.cleaned_data['equipos']:
                estadistica = Estadisticas(equipo=equipo,torneo=torneo)
                estadistica.save()
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
            torneo = form.save(commit=False)
            torneo.save()
            registros = Estadisticas.objects.filter(torneo=torneo)
            equipos = []
            for registro in registros:
                equipo = Equipo.objects.get(id=registro.equipo.id)
                equipos.append(equipo)
            for equipo in form.cleaned_data['equipos']:
                if equipo not in equipos:
                    estadistica = Estadisticas(equipo=equipo,torneo=torneo)
                    estadistica.save()
            for equipo in equipos:
                if equipo not in form.cleaned_data['equipos']:
                    e = Estadisticas.objects.get(equipo=equipo,torneo=torneo)
                    e.delete()
            messages.success(request, 'Torneo agregado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))

            messages.success(request, 'Torneo editado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'torneo/torneo_editar.html', {'form': form, 'torneo':instance})

def eliminar_torneo(request,id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    for equipo in torneo.equipos.all():
        registro = Estadisticas.objects.get(torneo=torneo,equipo=equipo)
        registro.delete()
    torneo.delete()
    messages.success(request, 'Torneo eliminado exitosamente')
    return HttpResponseRedirect(reverse('torneo:lista_torneos'))

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
        fecha = fecha_inicial
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
        html = render_to_string('torneo/lista_partidos.html', {'partidos':partidos,'jornada':jornada,'id_jornada':id_jornada})
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

    torneo = get_object_or_404(Torneo, id=torneo_id)
    jornada = get_object_or_404(torneo.jornada_set.all(), id=jornada_id)

    html_template = render_to_string('torneo/pdf_template.html', {'torneo':torneo,'jornada':jornada})
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

def registrar_cedula(request, id_partido):
    return

def registrar_eventos(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    amarillas = Tarjetas_amarillas.objects.filter(partido=partido)
    rojas = Tarjetas_rojas.objects.filter(partido=partido)
    azules = Tarjetas_azules.objects.filter(partido=partido)
    goles = Goles.objects.filter(partido=partido)
    asistencias = Asistencia.objects.filter(partido=partido)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad'))
        evento = int(request.POST.get('evento'))
        id_jugadora = int(request.POST.get('jugadora'))
        jugadora = get_object_or_404(Jugadora, id=id_jugadora)
        tarjetas_rojas = Tarjetas_rojas.objects.filter(partido=partido, jugadora=jugadora).count()
        tarjetas_azules = Tarjetas_azules.objects.filter(partido=partido, jugadora=jugadora).count()
        goles_local = Goles.objects.values('cantidad').filter(equipo=partido.equipo_local).aggregate(cantidad=Sum('cantidad'))
        if goles_local['cantidad'] is None: goles_local['cantidad'] = 0
        goles_visitante = Goles.objects.values('cantidad').filter(equipo=partido.equipo_visitante).aggregate(cantidad=Sum('cantidad'))
        if goles_visitante['cantidad'] is None: goles_visitante['cantidad'] = 0

        if evento == 1:
            if cantidad > 0:
                registro = Asistencia.objects.get(partido=partido,jugadora=jugadora)
                if registro.equipo == partido.equipo_local:
                    if goles_local['cantidad'] + cantidad <= partido.goles_local:
                        gol = gol = Goles.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad, equipo=registro.equipo)
                        gol.save()
                elif registro.equipo == partido.equipo_visitante:
                    if goles_visitante['cantidad'] + cantidad <= partido.goles_visitante:
                        gol = gol = Goles.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad, equipo=registro.equipo)
                        gol.save()

        elif evento == 2:
            if cantidad > 0 and tarjetas_rojas == 0:
                tarjetas = Tarjetas_amarillas.objects.filter(partido=partido, jugadora=jugadora).aggregate(cantidad=Sum('cantidad'))
                if tarjetas['cantidad'] is None: tarjetas['cantidad'] = 0
                if tarjetas['cantidad'] == 0:
                    if cantidad == 1:
                        amarilla = Tarjetas_amarillas.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad)
                        amarilla.save()
                    elif cantidad == 2:
                        amarilla = Tarjetas_amarillas.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad)
                        amarilla.save()
                        roja = Tarjetas_rojas.objects.create(partido=partido, jugadora=jugadora)
                        roja.save()
                elif tarjetas['cantidad'] == 1:
                    if cantidad == 1:
                        amarilla = Tarjetas_amarillas.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad)
                        amarilla.save()
                        roja = Tarjetas_rojas.objects.create(partido=partido, jugadora=jugadora)
                        roja.save()

        elif evento == 3:
            if tarjetas_rojas == 0:
                roja = Tarjetas_rojas.objects.create(partido=partido, jugadora=jugadora, directa=True)
                roja.save()

        elif evento == 4:
            if tarjetas_azules == 0:
                azul = Tarjetas_azules.objects.create(partido=partido, jugadora=jugadora)
                azul.save()

        amarillas = Tarjetas_amarillas.objects.filter(partido=partido)
        rojas = Tarjetas_rojas.objects.filter(partido=partido)
        azules = Tarjetas_azules.objects.filter(partido=partido)
        goles = Goles.objects.filter(partido=partido)
        asistencias = Asistencia.objects.filter(partido=partido)

        html = render_to_string('torneo/lista_eventos.html', {'amarillas':amarillas,'rojas':rojas,'azules':azules,'goles':goles,'asistencias':asistencias, 'partido':partido})
        return HttpResponse(html)

    return render(request, 'torneo/registrar_eventos.html', {'amarillas':amarillas,'rojas':rojas,'azules':azules,'goles':goles,'asistencias':asistencias, 'partido':partido})

def eliminar_evento(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    if request.method == 'POST':
        evento = int(request.POST.get('evento'))
        id = int(request.POST.get('id'))

        if evento == 1:
            gol = Goles.objects.get(id=id)
            gol.delete()

        elif evento == 2:
            tarjeta = Tarjetas_amarillas.objects.get(id=id)
            tarjeta.delete()

        elif evento == 3:
            tarjeta = Tarjetas_rojas.objects.get(id=id)
            tarjeta.delete()

        elif evento == 4:
            tarjeta = Tarjetas_azules.objects.get(id=id)
            tarjeta.delete()

        amarillas = Tarjetas_amarillas.objects.filter(partido=partido)
        rojas = Tarjetas_rojas.objects.filter(partido=partido)
        azules = Tarjetas_azules.objects.filter(partido=partido)
        goles = Goles.objects.filter(partido=partido)
        asistencias = Asistencia.objects.filter(partido=partido)

        html = render_to_string('torneo/lista_eventos.html', {'amarillas':amarillas,'rojas':rojas,'azules':azules,'goles':goles,'asistencias':asistencias, 'partido':id_partido, 'partido':partido})
        return HttpResponse(html)
