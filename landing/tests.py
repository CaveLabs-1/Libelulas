from django.test import TestCase
from equipo.models import Equipo
from jugadora.models import Jugadora
import datetime
# Create your tests here.

class LandingTestCase(TestCase):
    def setUp(self):
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
