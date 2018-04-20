from django.test import TestCase
from torneo.models import *
from django.test import Client
from .models import *
from django.contrib.auth.models import User, Group
from django.db import models;
from jugadora.models import Jugadora;
from equipo.models import Equipo;
from django.core.files.uploadedfile import SimpleUploadedFile;
from django.urls import reverse

class TestPreRegistroCase(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

        a = Jugadora.objects.create(
            Nombre = 'Nombre A',
            Apellido = 'Apellido A',
            Nacimiento = '1997-01-01',
            Numero = 1,
            Posicion = 1,
            Notas = 'Ejemplo A Jugadora',
            Imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora1.jpg', 'rb').read(), content_type='image/jpeg')

        );
        a.save();
        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="1995",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        t1.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()


    def test_acceso_preregistro_no_login(self):
        torneo = Torneo.objects.get(id=2)
        response = self.client.get(reverse('coaches:pre_registro',kwargs={'id_torneo':torneo.id}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('coaches:pre_registro',kwargs={'id_torneo':torneo.id}))
        self.assertEqual(response.status_code, 200)

    def test_registro_pre_registro(self):
        torneo = Torneo.objects.get(id=2)
        self.client.post(reverse('coaches:pre_registro',kwargs={'id_torneo':torneo.id}), {"nombre": "Carlos", "correo": "croman@hotmail.com", "notas":"Esto es una prueba"})
        self.assertEqual(PreRegistro.objects.all().count(), 1)

class TestPreRegistroJugadoraCase(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

        a = Jugadora.objects.create(
            Nombre = 'Nombre A',
            Apellido = 'Apellido A',
            Nacimiento = '1997-01-01',
            Numero = 1,
            Posicion = 1,
            Notas = 'Ejemplo A Jugadora',
            Imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora1.jpg', 'rb').read(), content_type='image/jpeg')

        );
        a.save();
        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="1995",
            fecha_inicio='2010-12-12',
            costo=int(12.12),
            fecha_junta='1995-11-11',
            costo_credencial=12,
            activo=True
        )
        t1.save()
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()
        a =PreRegistro.objects.create(
            nombre="Ale",
            correo="Notas",
            notas="Aqui va las notas",
            torneo=t1,
            codigo="abc"
        )
        a.save()



    def test_pre_registro_jugadora(self):
        self.client.logout()
        ea = Equipo.objects.create(
            nombre = 'Equipo A',
           representante = 'Juan A',
           telefono = '4426483003',
           correo = 'rr100@live.com.mx',
           logo =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/balon1.jpg', 'rb').read(), content_type='image/jpeg'),
           colorLocal  = 1,
           colorVisitante = 2,
           cancha = 'Estadio Azteca',
           dia = 1,
           hora = '13:05',
           activo = False
           )
        ea.save();
        registro = PreRegistro.objects.get(codigo="abc")
        response = self.client.get(reverse('coaches:registrar_jugadora',kwargs={'id_equipo':ea.id,'codigo':registro.codigo}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, ea.jugadoras.all().count())
        data = {
            'Nombre': 'Ale',
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '4',
            'Notas': 'Esto es una nota',
            'equipo':'1',
            'activo':False
        }
        self.client.post(reverse('coaches:registrar_jugadora',kwargs={'id_equipo':ea.id,'codigo':registro.codigo}),data)
        self.assertEqual(1, ea.jugadoras.all().count())


    def test_pre_registro_jugadora_incompleto(self):
        self.client.logout()
        ea = Equipo.objects.create(
            nombre = 'Equipo A',
           representante = 'Juan A',
           telefono = '4426483003',
           correo = 'rr100@live.com.mx',
           logo =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/balon1.jpg', 'rb').read(), content_type='image/jpeg'),
           colorLocal  = 1,
           colorVisitante = 2,
           cancha = 'Estadio Azteca',
           dia = 1,
           hora = '13:05',
           activo = False
           )
        ea.save();
        registro = PreRegistro.objects.get(codigo="abc")
        response = self.client.get(reverse('coaches:registrar_jugadora',kwargs={'id_equipo':ea.id,'codigo':registro.codigo}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, ea.jugadoras.all().count())
        data = {
            'Apellido': 'López',
            'Nacimiento': '1111-11-11',
            'Numero': '1',
            'Posicion': '4',
            'Notas': 'Esto es una nota',
            'equipo':'1',
            'activo':False
        }
        self.client.post(reverse('coaches:registrar_jugadora',kwargs={'id_equipo':ea.id,'codigo':registro.codigo}),data)
        self.assertEqual(0, ea.jugadoras.all().count())
