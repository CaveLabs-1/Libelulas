from django.shortcuts import render
from .forms import *
from django.urls import reverse
from django.http import *
from django.contrib import messages
from django.shortcuts import *
from torneo.models import *
from equipo.models import *
from jugadora.models import *
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Sum, Count
from django.utils import timezone
from torneo.forms import *
import datetime
import uuid
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse

#Desplegar la lista de torneos
def lista_torneos(request):
    lista_torneos = Torneo.objects.all()
    return render(request, 'torneo/torneo_list.html', {'lista_torneos': lista_torneos})

#Detalle de un torneo en específico
def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    return render(request, 'torneo/torneo_detail.html', {'torneo': torneo, 'equipos':torneo.equipos.all})

#Crear un torneo
def crear_torneo(request):
    lista_equipo = Equipo.objects.all()
    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES)
        if form.is_valid():
            torneo = form.save(commit=False)
            torneo.save()
            if form.cleaned_data['equipos']:
                #Crear los registros de estadísticas por equipo registrado en el torneo
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

#Actualizar la información de un torneo
def editar_torneo(request, torneo_id):
    instance = get_object_or_404(Torneo, id=torneo_id)
    form = torneoForm(instance=instance)
    if request.method == "POST":
        form = torneoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            torneo = form.save(commit=False)
            torneo.save()
            #Obtener los registros de estadísticas
            registros = Estadisticas.objects.filter(torneo=torneo)
            equipos = []
            #Obtener una lista de equipos registrados en el torneo
            for registro in registros:
                equipo = Equipo.objects.get(id=registro.equipo.id)
                equipos.append(equipo)
            #Registar equipos que no existen en estadísticas
            for equipo in form.cleaned_data['equipos']:
                if equipo not in equipos:
                    estadistica = Estadisticas(equipo=equipo,torneo=torneo)
                    estadistica.save()
            #Remover los equipos que no están registrados en el torneo
            for equipo in equipos:
                if equipo not in form.cleaned_data['equipos']:
                    e = Estadisticas.objects.get(equipo=equipo,torneo=torneo)
                    e.delete()
            messages.success(request, 'Torneo editado exitosamente')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    return render(request, 'torneo/torneo_editar.html', {'form': form, 'torneo':instance})

#Eliminar torneo
def eliminar_torneo(request,id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    #Eliminar los objetos de estadísticas
    for equipo in torneo.equipos.all():
        registro = Estadisticas.objects.get(torneo=torneo,equipo=equipo)
        registro.delete()
    torneo.delete()
    messages.warning(request, 'Torneo eliminado exitosamente')
    return HttpResponseRedirect(reverse('torneo:lista_torneos'))

#Eliminar equipo de un torneo
def eliminar_equipo(request, id_equipo, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    equipo = get_object_or_404(Equipo, id=id_equipo)
    if equipo in torneo.equipos.all():
        torneo.equipos.remove(equipo)
        messages.success(request, 'Equipo eliminado exitosamente')
        return HttpResponseRedirect(reverse('torneo:detalle_torneo',kwargs={'torneo_id':id_torneo}))

#Registrar un partido nuevo
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

#Cerrar el registro de un torneo y generar el rol de juegos
def cerrar_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    if torneo.activo:
        fecha_inicial = torneo.fecha_inicio
        fecha_fin =  fecha_inicial + timezone.timedelta(days=6)
        equipos = torneo.equipos.all()
        #Validar que almenos haya 2 equipos registrados en el torneo
        if len(equipos) >= 2:
            torneo.activo = False
            torneo.save()
            id_last_j = 1
            lista = []
            for equipo in equipos:
                lista.append(equipo.nombre)
            lista_vuelta = []
            for equipo in equipos:
                lista_vuelta.append(equipo.nombre)
            lista_vuelta = lista_vuelta[::-1]
            #Crear las jornadas de ida
            jornadas_local = create_schedule(lista)
            #Crear las jornadas de vuelta
            jornadas_visitante = create_schedule(lista_vuelta)
            id_last_j,fecha_inicial,fecha_fin = partidos(id_last_j,jornadas_local,fecha_inicial,fecha_fin,torneo)
            #Crear los partidos por semana
            partidos(id_last_j,jornadas_visitante,fecha_inicial,fecha_fin,torneo)
            messages.success(request,'El registro del torneo ha sido cerrado')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))
        else:
            messages.warning(request, 'El registro debe de tener mas de un equipo para ser registrado')
            return HttpResponseRedirect(reverse('torneo:lista_torneos'))

#Metodo para poder crear las jornadas dependiendo del número de equipos
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

#Método para poder crear los partidos dependiendo de el número de jornadas
def partidos(id_last_j,jornadas_local,fecha_inicial,fecha_fin,torneo):
    for i,semana in enumerate(jornadas_local):
        #Nombre de la jornada
        descripcion = "J"+str(id_last_j)
        jornada = Jornada(jornada=descripcion,torneo=torneo,fecha_inicio=fecha_inicial,fecha_fin=fecha_fin)
        #Crear el objeto jornada
        fecha_inicial = fecha_fin + timezone.timedelta(days=1)
        fecha_fin =  fecha_inicial + timezone.timedelta(days=6)
        fecha = fecha_inicial
        jornada.save()
        #Crear los partidos
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

#Editar el rol de juegos
def editar_registro(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    jornadas = Jornada.objects.filter(torneo=torneo)
    return render(request, 'torneo/editar_registro.html', {'jornadas':jornadas, 'torneo':torneo})

#Cargar la lista de partidos de una cierta jornada
def carga_partidos(request):
    if request.method == 'POST':
        id_jornada= int(request.POST.get('jornada'))
        jornada = get_object_or_404(Jornada, id=id_jornada)
        torneo=jornada.torneo_id
        partidos = Partido.objects.filter(jornada=jornada)
        html = render_to_string('torneo/lista_partidos.html', {'partidos':partidos,'jornada':jornada,'id_jornada':id_jornada})
        return HttpResponse(html)

#Editar los datos de un partido en específico
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

#Generar el pdf con los códigos de una cierta jornada para editar las cédulas
def mandar_codigoCedula(request, torneo_id, jornada_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)
    jornada = get_object_or_404(torneo.jornada_set.all(), id=jornada_id)

    html_template = render_to_string('torneo/pdf_template.html', {'torneo':torneo,'jornada':jornada})
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

#Generar el pdf de la cedula vacía con los datos de las jugadoras y equipos
def mandar_Cedula(request, partido_id):

    partido = Partido.objects.get(id = partido_id)

    html_template = render_to_string('torneo/CedulaPDF_template.html', {'partido':partido})
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

#Interfaz en la que se puede acceder a una cierta cédula
def accesar_cedula(request):
    if request.method == 'POST':
          form = AccesarCedula(data=request.POST)
          if form.is_valid():
              id_partido = form.cleaned_data['id_partido']
              id_torneo = form.cleaned_data['id_torneo']
              partido = get_object_or_404(Partido, id=id_partido)
              return HttpResponseRedirect(reverse('torneo:registrar_cedula',kwargs={'id_torneo':id_torneo, 'id_partido':id_partido}))
    form = AccesarCedula()
    return render(request, 'torneo/accesar_cedula.html', {'form':form})

#Registrar los datos de un partido. Las asistencias, marcador y arbitro.
#Actualizar los datos de las estadísitcas del torneo.
def registrar_cedula(request, id_torneo, id_partido):
    if request.method == 'POST':
        form = CedulaForm(data=request.POST)
        if form.is_valid():
            # Obtener instancia del partido a actualizar.
            update = Partido.objects.get(id=id_partido)
            # Guarda los datos del partido original. Los usaremos en caso de que sea actualización y no registro.
            goles_local_anterior = update.goles_local
            goles_visitante_anterior = update.goles_visitante
            # Actualiza la información del partido.
            update.goles_local = form.cleaned_data['goles_local']
            update.goles_visitante = form.cleaned_data['goles_visitante']
            update.notas = form.cleaned_data['notas']
            update.arbitro = form.cleaned_data['arbitro']
            update.save()
            messages.success(request, 'Cédula registrada exitosamente.')
            # Obtener estadísticas del equipo local.
            equipo_local = update.equipo_local_id
            estadisticas_local = Estadisticas.objects.get(torneo=id_torneo, equipo=equipo_local)
            # Obtener estadísticas del equipo visitante.
            equipo_visitante = update.equipo_visitante_id
            estadisticas_visitante = Estadisticas.objects.get(torneo=id_torneo, equipo=equipo_visitante)
            # Si es actualización, primero elimina las estadísticas registradas previamente.
            if update.registrado == True:
                estadisticas_local.goles_favor = estadisticas_local.goles_favor - goles_local_anterior
                estadisticas_local.goles_contra = estadisticas_local.goles_contra - goles_visitante_anterior
                estadisticas_visitante.goles_favor = estadisticas_visitante.goles_favor - goles_visitante_anterior
                estadisticas_visitante.goles_contra = estadisticas_visitante.goles_contra - goles_local_anterior
                # Restablece los puntos y partidos ganados/perdidos en caso de que gane haya ganado el local.
                if goles_local_anterior > goles_visitante_anterior:
                    # Actualizar estadísticas local (Ganador)
                    estadisticas_local.puntos = estadisticas_local.puntos - 3
                    estadisticas_local.ganados = estadisticas_local.ganados - 1
                    # Actualizar estadísticas visitante (Perdedor)
                    estadisticas_visitante.perdidos = estadisticas_visitante.perdidos - 1
                # Restablece los puntos y partidos ganados/perdidos en caso de que gane haya ganado el visitante.
                elif goles_visitante_anterior > goles_local_anterior:
                    # Actualizar estadísticas visitante (Ganador)
                    estadisticas_visitante.puntos = estadisticas_visitante.puntos - 3
                    estadisticas_visitante.ganados = estadisticas_visitante.ganados - 1
                    # Actualizar estadísticas local (Perdedor)
                    estadisticas_local.perdidos = estadisticas_local.perdidos - 1
                # Restablece los puntos y partidos ganados/perdidos en caso de que gane haya ganado sido empate.
                else:
                    # Actualizar estadísticas local (Empate)
                    estadisticas_local.puntos = estadisticas_local.puntos - 1
                    estadisticas_local.empatados = estadisticas_local.ganados - 1
                    # Actualizar estadísticas visitante (Empate)
                    estadisticas_visitante.puntos = estadisticas_visitante.puntos - 1
                    estadisticas_visitante.empatados = estadisticas_local.ganados - 1
                # Guardar Cambios
                estadisticas_local.save()
                estadisticas_visitante.save()
            else:
                # Prende la bandera de que el juego ya fue registrado y a partir de ahora se actualizará.
                update.registrado = True
                update.save()
                # Actualiza partidos jugados de ambos equipos.
                estadisticas_local.jugados = estadisticas_local.jugados + 1
                estadisticas_visitante.jugados = estadisticas_visitante.jugados + 1
            # Ahora sí actualizamos las estadísticas con los campos actualizados del partido.
            estadisticas_local.goles_favor = estadisticas_local.goles_favor + update.goles_local
            estadisticas_local.goles_contra = estadisticas_local.goles_contra + update.goles_visitante
            estadisticas_visitante.goles_favor = estadisticas_visitante.goles_favor + update.goles_visitante
            estadisticas_visitante.goles_contra = estadisticas_visitante.goles_contra + update.goles_local
            # Gana el Local
            if update.goles_local > update.goles_visitante:
                # Actualizar Estadísiticas Local (Ganador)
                estadisticas_local.puntos = estadisticas_local.puntos + 3
                estadisticas_local.ganados = estadisticas_local.ganados + 1
                # Actualizar Estadísiticas Visitante (Perdedor)
                estadisticas_visitante.perdidos = estadisticas_visitante.perdidos + 1
            # Gana el Visitante
            elif update.goles_visitante > update.goles_local:
                # Actualizar Estadísiticas Visitante (Ganador)
                estadisticas_visitante.puntos = estadisticas_visitante.puntos + 3
                estadisticas_visitante.ganados = estadisticas_visitante.ganados + 1
                # Actualizar Estadísiticas Local (Perdedor)
                estadisticas_local.perdidos = estadisticas_local.perdidos + 1
            # Visitante
            else:
                # Actualizar Estadísiticas Local (Empate)
                estadisticas_local.puntos = estadisticas_local.puntos + 1
                estadisticas_local.empatados = estadisticas_local.ganados + 1
                # Actualizar Estadísiticas Visitante (Empate)
                estadisticas_visitante.puntos = estadisticas_visitante.puntos + 1
                estadisticas_visitante.empatados = estadisticas_local.ganados + 1
            # Guardar Cambios
            estadisticas_local.save()
            estadisticas_visitante.save()
            return HttpResponseRedirect(reverse('torneo:registrar_eventos',kwargs={'id_partido':id_partido}))
        else:
            return HttpResponse(form.errors.as_text())
    else:
        form = CedulaForm()
        partido = Partido.objects.get(id=id_partido)
        equipo_local_id = Partido.objects.get(id=id_partido).equipo_local_id
        equipo_local = Equipo.objects.get(pk=equipo_local_id)
        jugadoras_locales = equipo_local.jugadoras.all()
        cant_jugadoras_locales = jugadoras_locales.count()
        equipo_visitante_id = Partido.objects.get(id=id_partido).equipo_visitante_id
        equipo_visitante = Equipo.objects.get(pk=equipo_visitante_id)
        jugadoras_visitantes = equipo_visitante.jugadoras.all()
        print(jugadoras_visitantes)
        cant_jugadoras_visitantes = jugadoras_visitantes.count()
        if cant_jugadoras_locales >= cant_jugadoras_visitantes:
            maximo = cant_jugadoras_locales
        else:
            maximo = cant_jugadoras_visitantes
        jugadoras = dict()
        cont = 0
        asistencia = 0
        for i in range(0,maximo):
            if i < cant_jugadoras_locales:
                asistencia = Asistencia.objects.filter(partido=id_partido,jugadora=jugadoras_locales[i].id,equipo=equipo_local_id)
                if asistencia:
                    asistencia = 1
                else:
                    asistencia = 0
                jugadoras[cont] = {'id':jugadoras_locales[i].id,'nombre':jugadoras_locales[i].Nombre + " " + jugadoras_locales[i].Apellido, 'numero':jugadoras_locales[i].Numero, 'equipo':equipo_local_id, 'asistencia':asistencia}
            else:
                jugadoras[cont] = {'id':'nada'}
            cont = cont + 1
            if i < cant_jugadoras_visitantes:
                asistencia = Asistencia.objects.filter(partido=id_partido,jugadora=jugadoras_visitantes[i].id,equipo=equipo_visitante_id)
                if asistencia:
                    asistencia = 1
                else:
                    asistencia = 0
                jugadoras[cont] = {'id':jugadoras_visitantes[i].id, 'nombre':jugadoras_visitantes[i].Nombre + " " + jugadoras_visitantes[i].Apellido, 'numero':jugadoras_visitantes[i].Numero, 'equipo':equipo_visitante_id, 'asistencia':asistencia}
            else:
                jugadoras[cont] = {'id':'nada'}
            cont = cont + 1
        informacion = {'id_torneo':id_torneo,'id_partido':id_partido,'partido':partido,'equipo_local':equipo_local,'equipo_visitante':equipo_visitante,'jugadoras':jugadoras,'form':form}
        return render(request, 'torneo/registrar_cedula.html', informacion)

#Registrar la asistencia de una jugadora en un partido
def registrar_asistencia(request):
    if request.method == "POST":
        id_equipo = request.POST.get('id_equipo')
        equipo = get_object_or_404(Equipo, id=id_equipo)
        id_partido = request.POST.get('id_partido')
        partido = get_object_or_404(Partido, id=id_partido)
        id_jugadora = request.POST.get('id_jugadora')
        jugadora = get_object_or_404(Jugadora, id=id_jugadora)
        estado = True if request.POST.get('estado') == 'true' else False
        status = "Hubo un error al actualizar la asistencia."
        #Si asistió la jugadora, se registra la asistencia
        if estado:
            asistencia = Asistencia.objects.create(partido=partido, jugadora=jugadora, equipo=equipo)
            asistencia.save()
            status = "Se registró la asistencia."
        else:
            asistencia = Asistencia.objects.get(partido=partido, jugadora=jugadora, equipo=equipo)
            asistencia.delete()
            status = "Se eliminó la asistencia."
    return HttpResponse(status)

#Registrar los eventos ocurridos en un partido, goles y tarjetas.
def registrar_eventos(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    amarillas = TarjetasAmarillas.objects.filter(partido=partido)
    rojas = TarjetasRojas.objects.filter(partido=partido)
    azules = Tarjetas_azules.objects.filter(partido=partido)
    goles = Goles.objects.filter(partido=partido)
    asistencias = Asistencia.objects.filter(partido=partido)

    if request.method == 'POST':
        #Obtener la cantidad de goles o tarjetas
        cantidad = int(request.POST.get('cantidad'))
        #Obtener el tipo de evento a registrar
        evento = int(request.POST.get('evento'))
        #Obtener el id de una jugadora
        id_jugadora = int(request.POST.get('jugadora'))
        jugadora = get_object_or_404(Jugadora, id=id_jugadora)
        #Obtener las tarjetas rojas y azules actuales de la jugadora
        tarjetas_rojas = TarjetasRojas.objects.filter(partido=partido, jugadora=jugadora).count()
        tarjetas_azules = Tarjetas_azules.objects.filter(partido=partido, jugadora=jugadora).count()
        #Obtener la suma total de goles registrados del equipo local
        goles_local = Goles.objects.values('cantidad').filter(equipo=partido.equipo_local).aggregate(cantidad=Sum('cantidad'))
        if goles_local['cantidad'] is None: goles_local['cantidad'] = 0
        #Obtener la suma total de goles registrados del equipo visitante
        goles_visitante = Goles.objects.values('cantidad').filter(equipo=partido.equipo_visitante).aggregate(cantidad=Sum('cantidad'))
        if goles_visitante['cantidad'] is None: goles_visitante['cantidad'] = 0

        #Si el evento es un gol
        if evento == 1:
            #Si la cantidad es mayor a 0
            if cantidad > 0:
                registro = Asistencia.objects.get(partido=partido,jugadora=jugadora)
                #Si la jugadora pertenece al equipo local
                if registro.equipo == partido.equipo_local:
                    #Si la cantidad no sobre pasa la cantidad de goles registrados
                    if goles_local['cantidad'] + cantidad <= partido.goles_local:
                        gol = gol = Goles.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad, equipo=registro.equipo)
                        gol.save()
                #Si la jugadora pertenece al equipo visitante
                elif registro.equipo == partido.equipo_visitante:
                    #Si la cantidad no sobre pasa la cantidad de goles registrados
                    if goles_visitante['cantidad'] + cantidad <= partido.goles_visitante:
                        gol = gol = Goles.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad, equipo=registro.equipo)
                        gol.save()
            else:
                messages.warning(request, 'Cantidad Inválida de goles')
                response = {'estatus':'ERROR'}
                return JsonResponse(response)

        #Si el evento es una tarjeta amarilla
        elif evento == 2:
            #Si la cantidad es mayor a 0 y no tiene registradas tarjetas rojas
            if cantidad > 0 and tarjetas_rojas == 0:
                #Obtener cantidad de tarjetas amarillas registradas
                tarjetas = TarjetasAmarillas.objects.filter(partido=partido, jugadora=jugadora).aggregate(cantidad=Sum('cantidad'))
                if tarjetas['cantidad'] is None: tarjetas['cantidad'] = 0
                #Si no tiene registrada ninguna tarjeta
                if tarjetas['cantidad'] == 0:
                    #Si quiere agregar una tarjeta amarilla
                    if cantidad == 1:
                        amarilla = TarjetasAmarillas.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad)
                        amarilla.save()
                    #Si quiere agregar 2 amarillas y 1 roja.
                    elif cantidad == 2:
                        amarilla = TarjetasAmarillas.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad)
                        amarilla.save()
                        roja = TarjetasRojas.objects.create(partido=partido, jugadora=jugadora)
                        roja.save()
                    else:
                        messages.warning(request, 'Cantidad inválida tarjetas amarillas')
                        response = {'estatus':'ERROR'}
                        return JsonResponse(response)
                #Si tiene registrada una tarjeta amarilla
                elif tarjetas['cantidad'] == 1:
                    #Si quiere registrar otra tarjeta amarilla
                    if cantidad == 1:
                        amarilla = TarjetasAmarillas.objects.create(partido=partido, jugadora=jugadora, cantidad=cantidad)
                        amarilla.save()
                        roja = TarjetasRojas.objects.create(partido=partido, jugadora=jugadora)
                        roja.save()
                    else:
                        messages.warning(request, 'Cantidad inválida tarjetas amarillas')
                        response = {'estatus':'ERROR'}
                        return JsonResponse(response)
                else:
                    messages.warning(request, 'Cantidad inválida tarjetas amarillas')
                    response = {'estatus':'ERROR'}
                    return JsonResponse(response)
            else:
                messages.warning(request, 'Cantidad inválida tarjetas rojas o amarillas')
                response = {'estatus':'ERROR'}
                return JsonResponse(response)
        #Si el evento es una tarjeta roja
        elif evento == 3:
            #Si no tiene registrada tarjetas rojas
            if tarjetas_rojas == 0:
                roja = TarjetasRojas.objects.create(partido=partido, jugadora=jugadora, directa=True)
                roja.save()
            else:
                messages.warning(request, 'Cantidad inválida tarjetas rojas')
                response = {'estatus':'ERROR'}
                return JsonResponse(response)
        #Si el evento es una tarjeta azul
        elif evento == 4:
            #Si no tiene registrada tarjetas azules
            if tarjetas_azules == 0:
                azul = Tarjetas_azules.objects.create(partido=partido, jugadora=jugadora)
                azul.save()
            else:
                messages.warning(request, 'Cantidad inválida tarjetas azules')
                response = {'estatus':'ERROR'}
                return JsonResponse(response)
        #Actualizar lista de objetos para actualizar el html
        amarillas = TarjetasAmarillas.objects.filter(partido=partido)
        rojas = TarjetasRojas.objects.filter(partido=partido)
        azules = Tarjetas_azules.objects.filter(partido=partido)
        goles = Goles.objects.filter(partido=partido)
        asistencias = Asistencia.objects.filter(partido=partido)
        #Html actualizado con la lista de eventos del partido
        html = render_to_string('torneo/lista_eventos.html', {'amarillas':amarillas,'rojas':rojas,'azules':azules,'goles':goles,'asistencias':asistencias, 'partido':partido})
        response = {'html':html,'estatus':'OK'}
        return JsonResponse(response)

    return render(request, 'torneo/registrar_eventos.html', {'amarillas':amarillas,'rojas':rojas,'azules':azules,'goles':goles,'asistencias':asistencias, 'partido':partido})

#Eliminar un evento de un partido
def eliminar_evento(request, id_partido):
    partido = get_object_or_404(Partido, id=id_partido)
    if request.method == 'POST':
        evento = int(request.POST.get('evento'))
        id = int(request.POST.get('id'))
        #Eliminar un gol
        if evento == 1:
            gol = Goles.objects.get(id=id)
            gol.delete()
        #Eliminar una tarjeta amarilla
        elif evento == 2:
            tarjeta = TarjetasAmarillas.objects.get(id=id)
            tarjeta.delete()
        #Eliminar una tarjeta roja
        elif evento == 3:
            tarjeta = TarjetasRojas.objects.get(id=id)
            tarjeta.delete()
        #Eliminar una tarjeta azul
        elif evento == 4:
            tarjeta = Tarjetas_azules.objects.get(id=id)
            tarjeta.delete()
        #Actualizar la lista de eventos
        amarillas = TarjetasAmarillas.objects.filter(partido=partido)
        rojas = TarjetasRojas.objects.filter(partido=partido)
        azules = Tarjetas_azules.objects.filter(partido=partido)
        goles = Goles.objects.filter(partido=partido)
        asistencias = Asistencia.objects.filter(partido=partido)
        #Html actualizado con la lista de eventos del partido
        html = render_to_string('torneo/lista_eventos.html', {'amarillas':amarillas,'rojas':rojas,'azules':azules,'goles':goles,'asistencias':asistencias, 'partido':id_partido, 'partido':partido})
        return HttpResponse(html)

#Crear una nueva jornada
def nueva_jornada(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    if request.method == "POST":
        form = JornadaForm(request.POST)
        if form.is_valid():
            jornada = form.save(commit=False)
            jornada.torneo = torneo
            jornada.save()
            messages.success(request, 'Jornada creada exitosamente.')
            return redirect('/torneo/editar_registro/'+str(id_torneo))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
        form = JornadaForm()
    return render(request, 'torneo/nueva_jornada.html', {'form': form, 'torneo':torneo})

#Crear un partido adentro de una jornada
def nuevo_partido(request, id_jornada):
    jornada = get_object_or_404(Jornada, id=id_jornada)
    if request.method == "POST":
        form = NuevoPartidoForm(request.POST)
        if form.is_valid():
            partido = form.save(commit=False)
            partido.jornada = jornada
            partido.id = uuid.uuid4().hex[:6].upper()
            partido.save()
            messages.success(request, 'Partido creado exitosamente.')
            return redirect('/torneo/editar_registro/'+str(jornada.torneo.id))
        else:
            messages.warning(request, 'Hubo un error en la forma')
    else:
        torneo = get_object_or_404(Torneo, id=jornada.torneo.id)
        equipos = torneo.equipos.all()
        form = NuevoPartidoForm()
        form.fields["equipo_visitante"].queryset = equipos
        form.fields["equipo_local"].queryset = equipos
    return render(request, 'torneo/nuevo_partido.html', {'form': form, 'jornada':jornada})

#Definir el ganador de un torneo
def ganador(request, id_torneo):
    torneo = get_object_or_404(Torneo, id=id_torneo)
    form = GanadorForm()
    if request.method == "POST":
        form = GanadorForm(request.POST)
        #Definir que ya existe un ganador en el torneo
        torneo.ganador = True
        torneo.save()
        team = request.POST.get('equipos')
        #Definir al equipo ganador
        stats =  get_object_or_404(Estadisticas, torneo=torneo, equipo=team)
        stats.ganador = True
        stats.save()
        messages.success(request, 'Ganador del torneo registrado exitosamente.')
        return redirect('/torneo/')
    else:
        equipos = torneo.equipos.all()
        form.fields["equipos"].queryset = equipos
    return render(request, 'torneo/ganador.html', {'form': form, 'torneo': torneo})
  
#Vista para poder acceder a una cedula con el cdigo del torneo y del partido
def cambio_cedula_admin(request, id_torneo, id_partido):
    return request(request, 'torneo/accesar_cedula.html')
