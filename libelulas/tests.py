from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class NoAuthenticationViewTests(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()

    def test_no_login(self):
        response = self.client.get(reverse('equipo:lista_equipos'))
        self.assertRedirects(response, '/login/?next=/equipo/')


class AuthenticationViewTests(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    def test_login(self):
        response = self.client.get(reverse('equipo:lista_equipos'))
        self.assertEqual(str(response.context['user']), 'testuser1')

    def test_logout(self):
        response = self.client.get(reverse('equipo:lista_equipos'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('equipo:lista_equipos'))
        self.assertRedirects(response, '/login/?next=/equipo/')
