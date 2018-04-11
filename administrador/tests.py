from django.test import TestCase

from administrador.models import User
from torneo.models import Torneo
from coaches.models import PreRegistro

class UserTestCase(TestCase):
    def test_create_user_correct_username(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Carlos", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().username, "croman")

    def test_create_user_correct_first_name(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Carlos", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "Carlos")

    def test_create_user_correct_email(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Carlos", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().email, "carlosromanrivera@hotmail.com")

    def test_create_user_existing_username(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Primero", "username": "croman", "email":"primero@hotmail.com"})
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Segundo", "username": "croman", "email":"segundo@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "Primero")

    def test_create_user_existing_email(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Primero", "username": "primero", "email":"carlosromanrivera@hotmail.com"})
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Segundo", "username": "segundo", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "Primero")

    def test_create_user_without_name(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "")

    def test_create_user_default_password(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().check_password("temporal"), True)

    def test_PreRegistro(self):

        usuario1 = User.objects.create_user(username='testuser2', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser2', password='12345')

        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="1995",
            fechaInicio='2010-12-12',
            costo=int(12.12),
            fechaJunta='1995-11-11',
            costoCredencial=12
        )

        a =PreRegistro.objects.create(
            Nombre="Ale",
            Correo="Notas",
            Notas="Aqui va las notas",
            torneo=t1
        )

        b = PreRegistro.objects.create(
            Nombre="Ale",
            Correo="gmail",
            Notas="Aqui va las notas",
            torneo=t1
        )

        a.save()
        b.save()

        resp = self.client.get('/administrador/lista_PreRegistro/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(a, b in resp.context['PreRegistros'])

        # Eliminar uno que no existe
        resp = self.client.get('/administrador/eliminar_PreRegistro/123123123/')
        self.assertEqual(resp.status_code, 404)

        # Eliminar uno correcto
        resp = self.client.get('/administrador/eliminar_PreRegistro/'+str(b.id)+'/')
        resp = self.client.get('/administrador/lista_PreRegistro/')
        self.assertTrue(a in resp.context['PreRegistros'])
        self.assertTrue(b not in resp.context['PreRegistros'])

        # Aceptar Un preregostr incorrecto
        resp = self.client.get('/administrador/aceptar_PreRegistro/123/')
        resp = self.client.get('/administrador/lista_PreRegistro/')
        c = PreRegistro.objects.get(id=a.id)
        self.assertTrue(c.codigo == None)


        # Aceptar Un preregostr correcto
        resp = self.client.get('/administrador/aceptar_PreRegistro/' + str(a.id) + '/')
        resp = self.client.get('/administrador/lista_PreRegistro/')
        c = PreRegistro.objects.get(id=a.id)
        self.assertFalse(c.codigo == None)