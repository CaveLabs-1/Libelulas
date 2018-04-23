from django.test import TestCase
from jugadora.models import Jugadora
from jugadora.forms import jugadoraForm
from django.test import Client
from equipo.models import Equipo
from django.contrib.auth.models import User, Group
import datetime
# Create your tests here.


class TestJugadoraCase(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

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
            'nombre': 'Alejandro',
            'apellido': 'López',
            'nacimiento': '09/22/1995',
            'numero': '-1',
            'posicion': '3',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con una posicion que no existe
        form_data = {
            'nombre': 'Alejandro',
            'apellido': 'López',
            'nacimiento': '09/22/1995',
            'numero': '-1',
            'posicion': '5',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con una fecha invalida
        form_data = {
            'nombre': 'Alejandro',
            'apellido': 'López',
            'nacimiento': '13/38/1995',
            'numero': '1',
            'posicion': '5',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con digitos en el nombre y apellido
        form_data = {
            'nombre': '123',
            'apellido': '123',
            'nacimiento': '13/38/1995',
            'numero': '1',
            'posicion': '3',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora con nombre y apellido mayor a 50
        form_data = {
            'nombre': 'Alejaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaandro',
            'apellido': 'Alejaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaandro',
            'nacimiento': '13/38/1995',
            'numero': '1',
            'posicion': '3',
            'equipo': ''
            }
        form = jugadoraForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Agregar jugadora sin imagen y Notas
        form_data = {
            'nombre': 'Alejandro',
            'apellido': 'López',
            'nacimiento': '1111-11-11',
            'numero': '1',
            'posicion': '3',
            'notas': 'Esto es una nota',
            }
        form = jugadoraForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())


        # Agregar jugadora con Imagen
        form_data = {
            'nombre': 'Alejandro',
            'apellido': 'López',
            'nacimiento': '1111-11-11',
            'numero': '1',
            'posicion': '3',
            'notas': 'Esto es una nota',

        }
        form = jugadoraForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Agregar jugadora sin imagen pero con notas
        form_data = {
            'nombre': 'Alejandro',
            'apellido': 'López',
            'nacimiento': '1111-11-11',
            'numero': '1',
            'posicion': '3',
            'notas': 'Esto es una nota',

            }
        form = jugadoraForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testEditarJugadora(self):


        j = Jugadora.objects.create(
                nombre = 'Alejandro',
                apellido = 'López',
                nacimiento = '1111-11-11',
                numero = '1',
                posicion = '3',
                notas = 'Esto es una nota',

                )

        form_data = {
            'nombre': '',
            'apellido': 'López',
            'nacimiento': '1111-11-11',
            'numero': '1',
            'posicion': '3',
            'notas': 'Esto es una nota',
            'imagen': 'ejemplo.jpg',

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
            'nombre': 'Ale',
            'apellido': 'López',
            'nacimiento': '1111-11-11',
            'numero': '1',
            'posicion': '5',
            'notas': 'Esto es una nota',

            }
        response = self.client.post('/jugadora/editar/1', form_data)
        # self.assertEqual(response['Location'], "/jugadora/editar/1")
        self.assertEqual(j, Jugadora.objects.get(id = 1))

        # Simular POST correcto
        form_data = {
            'nombre': 'Ale',
            'apellido': 'López',
            'nacimiento': '1111-11-11',
            'numero': '1',
            'posicion': '4',
            'notas': 'Esto es una nota',
            'equipo':'1'
            }
        response = self.client.post('/jugadora/editar/1', form_data)
        self.assertNotEqual(j.posicion, 3)

    def testVerJugadora(self):


        j = Jugadora.objects.create(
        nombre = 'Alejandro',
        apellido = 'López',
        nacimiento = '1111-11-11',
        numero = '1',
        posicion = '3',
        notas = 'Esto es una nota',

        )
        j1 = Jugadora.objects.create(
        nombre = 'Ramon',
        apellido = 'Romero',
        nacimiento = '1111-11-11',
        numero = '2',
        posicion = '4',
        notas = 'Esto es una nota',

        )



        # Simular el ir a la pagina
        response = self.client.get('/jugadora/ver_jugadoras', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jugadoras'].count(), Jugadora.objects.all().count())
        self.assertTemplateUsed(response, 'jugadora/ver_jugadoras.html')

    def testDeleteJugadora(self):
        j = Jugadora.objects.create(
            id=1,
            nombre='Ramon',
            apellido='Romero',
            nacimiento='1111-11-11',
            numero='2',
            posicion='4',
            notas='Esto es una nota',
        )

        j = Jugadora.objects.create(
            id=2,
            nombre='Ramon',
            apellido='Romero',
            nacimiento='1111-11-11',
            numero='2',
            posicion='4',
            notas='Esto es una nota',
        )


        #Revisar que existe la jugadora creadad
        self.assertTrue(Jugadora.objects.count() == 2)

        #Mandar un post para eliminar a la jugadora
        response = self.client.post('/jugadora/eliminar/1')
        self.assertTrue(Jugadora.objects.count() == 1)
