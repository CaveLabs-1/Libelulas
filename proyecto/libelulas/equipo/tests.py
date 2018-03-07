from django.test import TestCase
from django.urls import reverse
import datetime


# Create your tests here.
class test(TestCase):


    def test(self):

        resp = self.client.post(reverse('equipo:agregar_equipo'), { 'nombre' : 'jsc', 'representante' : 'njn', 'telefono' : '+219210219210', 'correo' : 'jj', 'logo' : 'media/equipo/view.jpg', 'colorLocal'  : 1, 'colorVisitante' : 1 ,'cancha' : 'cancua' ,'dia' : 1 , 'hora' : datetime.datetime.now()})
        self.assertEqual(resp.status_code, 200)

