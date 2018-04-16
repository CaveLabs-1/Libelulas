from django.test import TestCase
from equipo.models import Equipo
from jugadora.models import Jugadora
from torneo.models import *
from freezegun import freeze_time
import datetime
from django.db.models import Sum
from django.db.models import Count
# Create your tests here.

class LandingTestCase(TestCase):
    def setUp(self):
        equipo1 = Equipo.objects.create(
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
        equipo2 = Equipo.objects.create(
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
        jugadora1 = Jugadora.objects.create(
            id=1,
            Nombre='Alejandro',
            Apellido='López',
            Nacimiento='1995-09-22',
            Numero='1',
            Posicion=3,
            FechaDeAfiliacion='2000-10-10',
            NumPoliza='asdf',
            NUI='1235',
        )
        jugadora2 = Jugadora.objects.create(
            id=2,
            Nombre='Ramón',
            Apellido='Romero',
            Nacimiento='1995-10-23',
            Numero='2',
            Posicion=3,
            FechaDeAfiliacion='2000-10-10',
            NumPoliza='asdfg',
            NUI='12356',
        )
        jugadora3 = Jugadora.objects.create(
            id=3,
            Nombre='Marco',
            Apellido='Mancha',
            Nacimiento='1995-08-20',
            Numero='5',
            Posicion=2,
            FechaDeAfiliacion='2000-10-10',
            NumPoliza='asdfj',
            NUI='12354',
        )
        equipo1.jugadoras.add(jugadora1)
        equipo2.jugadoras.add(jugadora2)
        equipo2.jugadoras.add(jugadora3)
        torneo = Torneo.objects.create(
            id=1,
            nombre='Libelulas',
            categoria= 95,
            fechaInicio = '2018-05-05',
            anexo = '',
            costo = '100.00',
            costoCredencial = '200.50',
            activo = False,
            fechaJunta = '2018-05-04',
        )
        Estadisticas.objects.create(
            torneo_id=1,
            equipo_id=1,
            jugados=2,
            puntos=3,
            ganados=1,
            empatados=0,
            perdidos=1,
            goles_favor=2,
            goles_contra=3,
            ganador=False,
        )
        Estadisticas.objects.create(
            torneo_id=1,
            equipo_id=2,
            jugados=2,
            puntos=4,
            ganados=1,
            empatados=0,
            perdidos=1,
            goles_favor=5,
            goles_contra=2,
            ganador=True,
        )
        Jornada.objects.create(
            jornada='1',
            fecha_inicio='2018-05-05',
            fecha_fin='2018-05-07',
            torneo_id='1'
        )
        Partido.objects.create(
            id='006369',
            jornada_id='1',
            equipo_local_id=1,
            equipo_visitante_id=2,
            goles_local=0,
            goles_visitante=1,
            notas='Esto es una nota',
            fecha='2018-05-05',
            hora='10:15',
            cancha='Loma Dorada',
        )
        Partido.objects.create(
            id='006370',
            jornada_id='1',
            equipo_local_id=1,
            equipo_visitante_id=2,
            goles_local=0,
            goles_visitante=1,
            notas='Esto es una nota',
            fecha='2017-05-05',
            hora='10:15',
            cancha='Loma Dorada',
        )
        Goles.objects.create(
            partido_id='006369',
            jugadora_id='2',
            cantidad='1',
            equipo_id='2',
        )
        Asistencia.objects.create(
            partido_id='006369',
            jugadora_id='1',
            equipo_id='1'
        )
        Asistencia.objects.create(
            partido_id='006369',
            jugadora_id='2',
            equipo_id='2',
        )
        Tarjetas_amarillas.objects.create(
            partido_id='006369',
            jugadora_id='1',
            cantidad='1'
        )
        Tarjetas_azules.objects.create(
            partido_id='006369',
            jugadora_id='2',
        )
        Tarjetas_rojas.objects.create(
            partido_id='006369',
            jugadora_id='1',
            directa=True,
        )

    def tearDown(self):
        Equipo.objects.all().delete()

    def test_ver_equipos(self):
        response = self.client.get('/equipos/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['equipos'], ['<Equipo: Real Madrid F.C.>', '<Equipo: Club America>'], ordered=False)

    def test_ver_equipo(self):
        response = self.client.get('/equipos/equipo/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['equipo'], Equipo.objects.all().get(id=1))

    @freeze_time("2018-05-01")
    def test_ver_main(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['partidos'], ['<Partido: 006369>'])

    @freeze_time("2018-05-01")
    def test_ver_jugadora(self):
        response = self.client.get('/equipos/equipo/1/jugadora/6')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/equipos/equipo/1/jugadora/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jugadora'], Jugadora.objects.get(id=1))
        self.assertEqual(response.context['tarjetas_rojas'], Tarjetas_rojas.objects.filter(jugadora_id=1).count())
        self.assertEqual(response.context['tarjetas_azul'], Tarjetas_azules.objects.filter(jugadora_id=1).count())
        self.assertEqual(response.context['tarjetas_amarillas'], Tarjetas_amarillas.objects.filter(jugadora_id=1).aggregate(Sum('cantidad'))['cantidad__sum'])
        self.assertEqual(response.context['goles'], Goles.objects.filter(jugadora_id=1).filter(equipo_id=1).aggregate(Sum('cantidad'))['cantidad__sum'])
        self.assertEqual(response.context['asistencia'], Asistencia.objects.filter(jugadora_id=1).filter(equipo_id=1).count())
        self.assertEqual(response.context['edad'], 22)
        self.assertEqual(response.context['equipo'], Equipo.objects.get(id=1))



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


        # Entrar a un Torneo NO cerrado
        resp = self.client.get('/torneos/5')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(t3,resp.context['torneo'])

    def test_ver_partido(self):
        response = self.client.get('/torneos/1/partido/0')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/torneos/1/partido/006369')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['equipo_local'], Equipo.objects.all().get(nombre='Real Madrid F.C.'))
        self.assertEqual(response.context['equipo_visitante'], Equipo.objects.all().get(nombre='Club America'))
        self.assertEqual(response.context['torneo'], Torneo.objects.all().get(id=1))
        self.assertQuerysetEqual(response.context['jugadoras_local'], ['<Jugadora: Alejandro1>'])
        self.assertQuerysetEqual(response.context['jugadoras_visitante'], ['<Jugadora: Ramón2>'])
        self.assertQuerysetEqual(response.context['tarjetas_azul_local'], [])
        self.assertQuerysetEqual(response.context['tarjetas_azul_visitante'].values('jugadora_id'), ["{'jugadora_id': 2}"])
        self.assertQuerysetEqual(response.context['tarjetas_rojas_local'].values('jugadora_id'), ["{'jugadora_id': 1}"])
        self.assertQuerysetEqual(response.context['tarjetas_rojas_visitante'], [])
        self.assertQuerysetEqual(response.context['tarjetas_amarillas_local'].values('cantidad'), ["{'cantidad': 1}"])
        self.assertQuerysetEqual(response.context['tarjetas_amarillas_visitante'], [])
        self.assertQuerysetEqual(response.context['goles_local'], [])
        self.assertQuerysetEqual(response.context['goles_visitante'].values('cantidad'), ["{'cantidad': 1}"])

    def test_pre_registro(self):
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

        t4 = Torneo.objects.create(
            id=6,
            nombre="Torneo PRueba",
            categoria="1995",
            fechaInicio='2017-12-12',
            costo=int(12.12),
            fechaJunta='2019-11-11',
            costoCredencial=12,
            activo=True
        )
        resp = self.client.get('/coaches/pre_registro/5')
        resp2 = self.client.get('/coaches/pre_registro/6')
        self.assertTrue(resp.status_code == 404)
        self.assertTrue(resp2.status_code == 200)
