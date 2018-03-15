from django.test import TestCase
from torneo.models import Torneo
from torneo.forms import torneoForm
from equipo.models import Equipo
import datetime

# Create your tests here.

class TestTorneoCase(TestCase):



    def testAgregarTorneo(self):
        e = Equipo.objects.create(
            id=3,
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

        #informacion erronea
        form_data = {
            'nombre': 'TorneoAlejandro',
            'categoria': -3,
            'fechaInicio': '12asd12/1995',
            'anexo': '',
            'costo': 100.4,
        }

        form = torneoForm(data=form_data)
        self.assertFalse(form.is_valid())

        # informacion faltante
        form_data = {
            'nombre': '',
            'categoria': 1995,
            'fechaInicio': '12/12/1995',
            'anexo':'',
            'costo': 100.4,
        }

        form = torneoForm(data=form_data)
        self.assertFalse(form.is_valid())

        #informacion correcta
        form_data = {
            'nombre': 'TorneoAlejandro',
            'categoria': 1995,
            'fechaInicio': '12/12/1995',
            'anexo':'',
            'costo': 100.4,
        }

        form = torneoForm(data=form_data)
        self.assertTrue(form.is_valid())

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
            categoria="1995",
            fechaInicio='2010-12-12',
            costo=int(12.12)
        )

        self.assertTrue(Torneo.objects.all().count() == 1)

        #Visualizar que el objeto si es mandado al template
        response = self.client.get('/torneo/')
        self.assertTrue(t1 in response.context['lista_torneos'])
        self.assertTrue(response.status_code == 200)




