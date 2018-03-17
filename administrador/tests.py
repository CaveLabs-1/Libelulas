from django.test import TestCase
from administrador.models import User

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

