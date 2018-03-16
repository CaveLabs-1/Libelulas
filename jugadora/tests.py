from django.test import TestCase
from jugadora.models import Jugadora
from jugadora.forms import jugadoraForm
from django.test import Client
from equipo.models import Equipo
import datetime
# Create your tests here.


class TestJugadoraCase(TestCase):

    def testAgregarJugadora(self):
        # Crear un equipo


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
            'Posicion': '3',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con una posicion que no existe
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '09/22/1995',
            'Numero': '-1',
            'Posicion': '5',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con una fecha invalida
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '13/38/1995',
            'Numero': '1',
            'Posicion': '5',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con digitos en el nombre y apellido
        form_data = {
            'Nombre': '123',
            'Apellido': '123',
            'Nacimiento': '13/38/1995',
            'Numero': '1',
            'Posicion': '3',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con nombre y apellido mayor a 50
        form_data = {
            'Nombre': 'Alejaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaandro',
            'Apellido': 'Alejaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaandro',
            'Nacimiento': '13/38/1995',
            'Numero': '1',
            'Posicion': '3',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora sin imagen y Notas
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '3',
            'Notas': 'Esto es una nota',
            }
        form = jugadoraForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())


        # Agregar jugadora con Imagen
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '3',
            'Notas': 'Esto es una nota',

        }
        form = jugadoraForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Agregar jugadora sin imagen pero con notas
        form_data = {
            'Nombre': 'Alejandro',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '3',
            'Notas': 'Esto es una nota',

            }
        form = jugadoraForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testEditarJugadora(self):


        j = Jugadora.objects.create(
                Nombre = 'Alejandro',
                Apellido = 'López',
                Nacimiento = '1111-11-11',
                Numero = '1',
                Posicion = '3',
                Notas = 'Esto es una nota',

                )

        form_data = {
            'Nombre': '',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '3',
            'Notas': 'Esto es una nota',
            'Imagen': 'ejemplo.jpg',

            }

        # Simular que la página funciona
        response = self.client.get('/jugadora/editar/1')
        self.assertTrue(response.status_code == 200)

        # Simular POST vacio
        response = self.client.post('/jugadora/editar/1')
        self.assertEqual(j, Jugadora.objects.get(id = '1'))

        # Simular POST incompleto
        response = self.client.post('/jugadora/editar/1', form_data)
        # self.assertEqual(response['Location'], "/jugadora/editar/1")
        self.assertEqual(j, Jugadora.objects.get(id = 1))

        # Simular POST inválido
        form_data = {
            'Nombre': 'Ale',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '5',
            'Notas': 'Esto es una nota',

            }
        response = self.client.post('/jugadora/editar/1', form_data)
        # self.assertEqual(response['Location'], "/jugadora/editar/1")
        self.assertEqual(j, Jugadora.objects.get(id = 1))

        # Simular POST correcto
        form_data = {
            'Nombre': 'Ale',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '4',
            'Notas': 'Esto es una nota',
            'equipo':'1'
            }
        response = self.client.post('/jugadora/editar/1', form_data)
        self.assertNotEqual(j.Posicion, 3)

    def testVerJugadora(self):


        j = Jugadora.objects.create(
        Nombre = 'Alejandro',
        Apellido = 'López',
        Nacimiento = '1111-11-11',
        Numero = '1',
        Posicion = '3',
        Notas = 'Esto es una nota',

        )
        j1 = Jugadora.objects.create(
        Nombre = 'Ramon',
        Apellido = 'Romero',
        Nacimiento = '1111-11-11',
        Numero = '2',
        Posicion = '4',
        Notas = 'Esto es una nota',

        )



        # Simular el ir a la pagina
        response = self.client.get('/jugadora/ver_jugadoras', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jugadoras'].count(), Jugadora.objects.all().count())
        self.assertTemplateUsed(response, 'jugadora/ver_jugadoras.html')

    def testDeleteJugadora(self):
        j = Jugadora.objects.create(
            id=1,
            Nombre='Ramon',
            Apellido='Romero',
            Nacimiento='1111-11-11',
            Numero='2',
            Posicion='4',
            Notas='Esto es una nota',
        )

        j = Jugadora.objects.create(
            id=2,
            Nombre='Ramon',
            Apellido='Romero',
            Nacimiento='1111-11-11',
            Numero='2',
            Posicion='4',
            Notas='Esto es una nota',
        )


        #Revisar que existe la jugadora creadad
        self.assertTrue(Jugadora.objects.count() == 2)

        #Mandar un post para eliminar a la jugadora
        response = self.client.post('/jugadora/eliminar/1')
        self.assertTrue(Jugadora.objects.count() == 1)
