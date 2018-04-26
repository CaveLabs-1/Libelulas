from django.test import TestCase
from torneo.models import *
from torneo.forms import torneoForm
from equipo.models import Equipo
from django.utils import timezone
import datetime
import os, glob
from django.contrib.auth.models import User, Group
from django.urls import reverse

class TestTorneoCase(TestCase):
    def setUp(self):
         usuario1 = User.objects.create_user(username='testuser2', password='12345', is_superuser=True)
         usuario1.save()
         login = self.client.login(username='testuser2', password='12345')



    def testAgregarTorneo(self):
        self.client.login(username='testuser2', password='12345')
        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=6,
            nombre='Equipos2',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )


        e.save()
        f.save()
        #Error en la forma
        form_data = {
            'nombre': 'Alejandro',
            'categoria': '10',
            'categoria_max': '17',
            'fecha_inicio': '1111/11-11',
            'costo': '5',
            'costo_credencial': '5',
            'equipos': {'5', '6'},
            'fecha_junta': '1111-11-11',

        }
        form = torneoForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Campo Faltante
        form_data = {
            'nombre': 'Alejandro',
            'categoria': '10',
            'categoria_max': '17',
            'fecha_inicio': '1111/11-11',
            'costo': '5',
            'costo_credencial': '5',
            'fecha_junta': '1111-11-11',

        }
        form = torneoForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Forma Correcta
        form_data = {
            'nombre': 'Alejandro',
            'categoria': '15',
            'categoria_max': '17',
            'fecha_inicio': '1111-11-11',
            'costo': '5',
            'costo_credencial': '5',
            'equipos': {'5','6'},
            'fecha_junta': '1111-11-11',

        }
        form = torneoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testPDFCodigosArbitros(self):
        self.client.login(username='testuser2', password='12345')

        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=6,
            nombre='Equipos2',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )

        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="10",
            categoria_max="17",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()





        resp = self.client.get('/torneo/cerrar_registro/2', follow=True)

        resp2 = self.client.get('/torneo/mandar_codigoCedula/2/'+str(t1.jornada_set.all().first().id))

        self.assertTrue(resp2.status_code == 200)

    def testEliminarTorneo(self):
        self.client.login(username='testuser2', password='12345')

        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=6,
            nombre='Equipos2',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )

        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="10",
            categoria_max="17",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()

        # Eliminar un torneo que no existe
        self.client.get('/torneo/eliminar/3')
        self.assertTrue(Torneo.objects.all().count() > 0)

        # Eliminar un torneo invalido
        self.client.get('/torneo/eliminar/asd')
        self.assertTrue(Torneo.objects.all().count() > 0)

        # Eliminar un torneo valido
        self.client.get('/torneo/eliminar/2')
        self.assertTrue(Torneo.objects.all().count() == 0)

    def testEditarTorneo(self):
        self.client.login(username='testuser2', password='12345')

        self.client.login(username='testuser2', password='12345')

        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=6,
            nombre='Equipos2',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )

        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="10",
            categoria_max="17",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()


        #Forma Invalidad
        form_data = {
            'nombre': 'Ale',
            'categoria': '10',
            'categoria_max': '17',
            'fecha_inicio': '1111-11-11',
            'fecha_junta': '1111-11-11',
            'costo': 1,
            'costo_credencial': 4,
            'equipos': {'alksdj', '6'}
        }

        self.assertTrue(t1.nombre == 'Torneo PRueba')
        response = self.client.post('/torneo/editar/2', form_data)
        self.assertFalse(Torneo.objects.get(id=2).nombre == 'Ale')


        #Forma Incompleta
        form_data = {
            'nombre': 'Ale',
            'categoria': '10',
            'fecha_inicio': '1111-11-11',
            'fecha_junta': '1111-11-11',
            'costo': 1,
            'costo_credencial': 4,
        }

        self.assertTrue(t1.nombre=='Torneo PRueba')
        response = self.client.post('/torneo/editar/2', form_data)
        self.assertFalse(Torneo.objects.get(id=2).nombre == 'Ale')

        #Forma Correcta
        form_data = {
            'nombre': 'Ale',
            'categoria': '10',
            'categoria_max': '17',
            'fecha_inicio': '1111-11-11',
            'fecha_junta': '1111-11-11',
            'costo': 1,
            'costo_credencial': 4,
            'equipos': {'5', '6'}
        }

        self.assertTrue(t1.nombre=='Torneo PRueba')
        response = self.client.post('/torneo/editar/2', form_data)
        self.assertTrue(Torneo.objects.get(id=2).nombre == 'Ale')







    def testCerrarRegistro(self):
        self.client.login(username='testuser2', password='12345')

        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=6,
            nombre='Equipos2',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )

        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="10",
            categoria_max="17",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()

        # Cerrar el registro de un torneo que no existe
        self.assertTrue(t1.jornada_set.all().count() == 0)
        self.client.get('/torneo/cerrar_registro/3')
        self.assertFalse(t1.jornada_set.all().count() > 0)

        # Cerrar el registro de un torneo que invalido
        self.assertTrue(t1.jornada_set.all().count() == 0)
        self.client.get('/torneo/cerrar_registro/asd')
        self.assertFalse(t1.jornada_set.all().count() > 0)

        # Cerrar un Torneo Valido
        self.assertTrue(t1.jornada_set.all().count() == 0)
        resp = self.client.get('/torneo/cerrar_registro/2', follow=True)
        self.assertTrue(t1.jornada_set.all().count() > 0)

    def testVerTorneo(self):
         e = Equipo.objects.create(
             id=5,
             nombre='Equipos',
             representante='Juanito López',
             telefono='4423471577',
             correo='juanito@mail.com',
             colorLocal='1',
             colorVisitante='1',
             cancha='Qro',
             dia='1',
             hora=datetime.datetime.now()
         )

         t1=Torneo.objects.create(
             id=2,
             nombre="Torneo PRueba",
             categoria="10",
             categoria_max="17",
             fecha_inicio='2010-12-12',
             costo=int(12.12),
             fecha_junta='1995-11-11',
             costo_credencial=12
         )

         self.assertTrue(Torneo.objects.all().count() == 1)

         #Visualizar que el objeto si es mandado al template
         response = self.client.get('/torneo/')
         self.assertTrue(t1 in response.context['lista_torneos'])
         self.assertTrue(response.status_code == 200)





class EditarPartidoTest(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')
        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=6,
            nombre='Equipos2',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )

        t1=Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="10",
            categoria_max="17",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()
        e1 = Estadisticas.objects.create(torneo=t1,equipo=e)
        e1.save()
        e2 = Estadisticas.objects.create(torneo=t1,equipo=e)
        e2.save()
        self.client.get(reverse('torneo:cerrar_registro',kwargs={'id_torneo':2}))

    def test_editar_partido_fecha_correcta(self):
        partido = Partido.objects.all()[:1].get()
        id_partido = partido.id
        fecha_anterior = partido.fecha
        fecha = partido.jornada.fecha_inicio + timezone.timedelta(days=3)
        form_data = {
            'fecha': fecha,
            'hora': partido.hora,
            'cancha': 'Santiago Bernabéu'
        }
        resp = self.client.post(reverse('torneo:editar_partido',kwargs={'id_partido':partido.id}),form_data)
        partido = Partido.objects.get(id=id_partido)
        self.assertEqual(partido.fecha, fecha)

    def test_checar_acceso_arbitro(self):
        self.client.logout()
        partido = Partido.objects.all()[:1].get()
        response = self.client.get(reverse('torneo:registrar_eventos',kwargs={'id_partido':partido.id}))
        self.assertEqual(str(response.context['partido']), partido.id)



    def test_PDF_Cedula(self):

        self.client.login(username='testuser2', password='12345')

        e = Equipo.objects.create(
            id=15,
            nombre='Equipoasds',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='1',
            hora=datetime.datetime.now()
        )
        f = Equipo.objects.create(
            id=20,
            nombre='Equipos55',
            representante='Juanito López',
            telefono='4423471577',
            correo='juanito@mail.com',
            colorLocal='1',
            colorVisitante='1',
            cancha='Qro',
            dia='2',
            hora=datetime.datetime.now()
        )

        t1 = Torneo.objects.create(
            id=5,
            nombre="Torneo PRueba133",
            categoria="10",
            categoria_max="17",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()

        resp = self.client.get('/torneo/cerrar_registro/5', follow=True)

        # Existe el partido
        resp2 = self.client.get('/torneo/mandar_Cedula/' + str(t1.jornada_set.all().first().partido_set.all().first()))
        self.assertTrue(resp2.status_code == 200)
