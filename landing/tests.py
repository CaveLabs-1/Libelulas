from django.test import TestCase
from equipo.models import Equipo
from jugadora.models import Jugadora
import datetime
from torneo.models import Torneo, Estadisticas
from django.contrib.auth.models import User, Group
from django.urls import reverse
# Create your tests here.

class LandingTestCase(TestCase):
    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser2', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser2', password='12345')

        Equipo.objects.create(
            id = 1,
            nombre ='Real Madrid F.C.',
            representante = 'Florentino Pérez',
            telefono = '+5144227654321',
            correo = 'florentinop@realmadrid.com',
            colorLocal = 1,
            colorVisitante = 2,
            cancha = 'Santiago Bernabéu',
            dia = 7,
            logo = 'media/equipo/ejemplo.jpg',
            hora = datetime.datetime.now().time()
        )
        Equipo.objects.create(
            id = 2,
            nombre ='Club America',
            representante = 'Mauricio Culebro',
            telefono = '+5144227654321',
            correo = 'america@fc.com',
            colorLocal = 1,
            colorVisitante = 2,
            cancha = 'Estadio Azteca',
            dia = 7,
            logo = 'media/equipo/ejemplo.jpg',
            hora = datetime.datetime.now().time()
        )

    def test_ver_equipos(self):
        response = self.client.get('/equipos/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['equipos'], ['<Equipo: Real Madrid F.C.>', '<Equipo: Club America>'], ordered=False)

    def test_ver_equipo(self):
        response = self.client.get('/equipos/equipo/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['equipo'], Equipo.objects.all().get(id=1))

    def test_ver_tablaGeneral(self):
        self.client.login(username='testuser2', password='12345')

        e = Equipo.objects.create(
            id=5,
            nombre='Equipos',
            representante='Juanito López',
            logo='j.jpg',
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
            logo='j.jpg',
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
            categoria="1995",
            fechaInicio='2017-12-12',
            costo=int(12.12),
            fechaJunta='1995-11-11',
            costoCredencial=12,
            activo=True
        )
        t3 = Torneo.objects.create(
            id=5,
            nombre="Torneo PRueba",
            categoria="1995",
            fechaInicio='2017-12-12',
            costo=int(12.12),
            fechaJunta='1995-11-11',
            costoCredencial=12,
            activo=True
        )
        e.save()
        f.save()
        t1.save()
        t3.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()

        resp = self.client.get('/torneo/cerrar_registro/2', follow=True)

        # Entrar a un Torneo No Existente
        resp = self.client.get('/torneos/3')
        self.assertEqual(resp.status_code, 404)

        # Entrar a un Torneo Ya cerrado
        resp = self.client.get('/torneos/2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(t1,resp.context['torneo'])
        self.assertTrue(resp.context['jornadas'].exists())

        # Entrar a un Torneo NO cerrado
        resp = self.client.get('/torneos/5')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(t3,resp.context['torneo'])
        self.assertFalse(resp.context['jornadas'].exists())