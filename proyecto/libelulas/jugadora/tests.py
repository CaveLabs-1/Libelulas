from django.test import TestCase
from jugadora.models import Jugadora
from jugadora.forms import jugadoraForm
# Create your tests here.


class TestJugadoraCase(TestCase):
    def testAgregarJugadora(self):
        # Agregar jugadora vacia
        form_data = {}
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora incompleta
        form_data = {'Nombre': 'Alejandro'}
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con numero negativo
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '09/22/1995',
            'Numero': '-1',
            'Posicion': '3'
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con una posicion que no existe
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '09/22/1995',
            'Numero': '-1',
            'Posicion': '5'
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con una fecha invalida
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '13/38/1995',
            'Numero': '1',
            'Posicion': '5'
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con digitos en el nombre y apellido
        form_data = {
            'Nombre': '123',
            'Apellido': '123',
            'Nacimiento': '13/38/1995',
            'Numero': '1',
            'Posicion': '3'
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con nombre y apellido mayor a 50
        form_data = {
            'Nombre': 'Alejaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaandro',
            'Apellido': 'Alejaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaandro',
            'Nacimiento': '13/38/1995',
            'Numero': '1',
            'Posicion': '3'
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora sin imagen y Notas
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '09/22/1995',
            'Numero': '1',
            'Posicion': '3'
            }
        form = jugadoraForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Agregar jugadora sin imagen pero con notas
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '09/22/1995',
            'Numero': '1',
            'Posicion': '3',
            'Notas': 'Esto es una nota'
            }
        form = jugadoraForm(data=form_data)
        self.assertTrue(form.is_valid())
