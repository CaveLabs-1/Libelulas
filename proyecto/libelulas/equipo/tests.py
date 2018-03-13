from django.test import TestCase
from django.urls import reverse
from django.shortcuts import render
from equipo.models import Equipo
from equipo.forms import equipoForm
import datetime
from django.shortcuts import render
from django.test import Client
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import sys
import os, glob

# Create your tests here.
class TestCrearEquipo(TestCase):
    
    def tearDown(self):
        Equipo.objects.all().delete()
        for filename in glob.glob("./media/media/equipo/test*"):
            os.remove(filename)    

    def test_happy_crear_equipo(self):
        #Revisar que no hay equipos
        self.assertEqual(Equipo.objects.count(), 0)
        #Hacer un update de una imagen correcta
        #Datos correctos
        form_data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
        #Pruebo que se vea el equipo despues de creado
        pk = Equipo.objects.get(nombre='Real Madrid Futboll Club').id
        response = self.client.get('/equipo/'+str(pk)+'/')
        self.assertEqual(response.status_code, 200)
    
    def test_no_nombre_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': '',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': '',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_numeros_en_nombre_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': '123',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': '123',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_nombre_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'a'*65,
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'a'*65,
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_especiales_en_nombre_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': '%#<>$%^&*.,/\\""()(&$!',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': '%#<>$%^&*.,/\\""()(&$!',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_representante_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': '',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_numeros_en_representate_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '123',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': '123',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_max_length_en_representante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C', 
            'representante': 'a'*65,
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'a'*65,
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_especiales_en_representante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '%#$%^&*""()(&$!',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': '%#$%^&*""()(&$!',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_acentos_en_representante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'éáíóúüñÉÍÁÓÚ',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'éáíóúüñÉÍÁÓÚ',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_telefono_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C',
            'representante': 'Florentino Pérez',
            'telefono': '',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_sin_extencion_de_pais_numero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C',
            'representante': 'Florentino Pérez',
            'telefono': '44227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '44227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '1'*18,
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '1'*18,
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': 'a',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': 'a',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_parentesis_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '(511234567890)',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '(511234567890)',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_espacios_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '442 2 123 123 1',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '442 2 123 123 1',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_correo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_con_doble_dominio_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo@itesm.com.mx',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo@itesm.com.mx',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
        
    def test_con_mayusculas_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'Ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'Ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
        
    def test_correo_empieza_con_punto_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_correo_con_punto_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_correo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': ('a'*128)+'@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': ('a'*128)+'@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_correo_con_numeros_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'gods42@answere.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'gods42@answere.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_color_local_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_negativo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '-1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '-1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_cero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '0',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '0',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)        
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_mayor_de_once_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '12',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '12',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_letras_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': 'a',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': 'a',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_caracteres_especiales_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '$',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '$',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)        
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_no_color_visitante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_negativo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '-2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '-2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_cero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '0',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '0',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_mayor_de_once_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '2',
            'colorVisitante': '12',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '12',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_letras_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': 'a',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': 'a',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_caracteres_especiales_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '$',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '$',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_cancha_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_numeros_en_cancha_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': '123',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '1234',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '1234',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_cancha_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'a'*129,
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'a'*129,
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_especiales_en_cancha_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '%#<>$%^&*.,/\\""()(&$!',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '%#<>$%^&*.,/\\""()(&$!',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_dia_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_negativo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '-1',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '-1',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_cero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '0',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '0',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_mayor_de_siete_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '8',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '8',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_letras_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': 'a',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': 'a',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_caracteres_especiales_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_logo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': ''
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_hora_negativa_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '-12:04'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '-12:04',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_letras_en_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': 'once am'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': 'once am',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_formato_doce_horas_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '10:54 am'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '10:54 am',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_horas_mayor_veinticuatro_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '27:12'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '27:12',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_minutos_mayor_a_59_casoA_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:60'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:60',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_minutos_mayor_a_59_casoB_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:61'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        
        data = {
            'nombre': 'Real Madrid Futboll Club',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:61',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), data)
        self.assertEqual(Equipo.objects.count(), 0)
    
class TestVerEquipo(TestCase):
    
    def setUp(self):
        imagen = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
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
            logo = imagen,
            hora = '13:00'
        )
    
    def tearDown(self):
        Equipo.objects.all().delete()
        for filename in glob.glob("./media/media/equipo/test*"):
            os.remove(filename) 
    
    def test_ver_existente_equipo(self):
        response = self.client.get('/equipo/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_ver_existente_equipo(self):
        response = self.client.get('/equipo/2/')
        self.assertEqual(response.status_code, 404)

class TestEditarEquipo(TestCase):
    
    def equipo1(self):
        imagen = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        equipo = Equipo.objects.create(
            id = 1,
            nombre ='Real Madrid F.C.',
            representante = 'Florentino Pérez',
            telefono = '+5144227654321',
            correo = 'florentinop@realmadrid.com',
            colorLocal = 1,
            colorVisitante = 2,
            cancha = 'Santiago Bernabéu',
            dia = 7,
            logo = imagen,
            hora = '13:18'
        )
        equipo.save()
        return equipo
    
    def equipo2(self):
        imagen = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        equipo = Equipo.objects.create(
            id = 2,
            nombre ='Juventus',
            representante = 'Florentino Pérez',
            telefono = '+5144227654321',
            correo = 'florentinop@realmadrid.com',
            colorLocal = 1,
            colorVisitante = 2,
            cancha = 'Santiago Bernabéu',
            dia = 7,
            logo = imagen,
            hora = '13:00'
        )
        equipo.save()
        return equipo
    
    def tearDown(self):
        Equipo.objects.all().delete()
        for filename in glob.glob("./media/media/equipo/test*"):
            os.remove(filename) 
    
    def test_cambio_nombre_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Success',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Success',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).nombre, 'Success')
    
    def test_no_nombre_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': '',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': '',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).nombre, 'Real Madrid F.C.')
    
    def test_numeros_en_nombre_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': '123',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': '123',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).nombre, '123')
    
    def test_max_length_en_nombre_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'a'*65,
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'a'*65,
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).nombre, 'Real Madrid F.C.')
        
    def test_caracteres_especiales_en_nombre_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': '%#<>$%^&*.,/\\""()(&$!',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': '%#<>$%^&*.,/\\""()(&$!',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).nombre, '%#<>$%^&*.,/\\""()(&$!')
    
    def test_editar_mismo_nombre_equipo(self):
        team = self.equipo1()
        team2 = self.equipo2()
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Juventus',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Juventus',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).nombre, 'Real Madrid F.C.')
    
    def test_cambio_representante_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Gillermo del Toro',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Gillermo del Toro',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).representante, 'Gillermo del Toro')
    
    def test_no_representante_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).representante, 'Florentino Pérez')
    
    def test_numeros_en_representate_equipo(self):
        team = self.equipo1()
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '123',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '123',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).representante, 'Florentino Pérez')
    
    def test_max_length_en_representante_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C', 
            'representante': 'a'*65,
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'a'*65,
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).representante, 'Florentino Pérez')
        
    def test_caracteres_especiales_en_representante_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '%#$%^&*""()(&$!',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '%#$%^&*""()(&$!',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).representante, 'Florentino Pérez')
        
    def test_acentos_en_representante_equipo(self):
        team = self.equipo1()
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'éáíóúüñÉÍÁÓÚ',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'éáíóúüñÉÍÁÓÚ',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).representante, 'éáíóúüñÉÍÁÓÚ')
    
    def test_cambio_telefono_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C',
            'representante': 'Florentino Pérez',
            'telefono': '+315524123654',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+315524123654',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '+315524123654')
    
    def test_no_telefono_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C',
            'representante': 'Florentino Pérez',
            'telefono': '',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '+5144227654321')
    
    def test_sin_extencion_de_pais_numero_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C',
            'representante': 'Florentino Pérez',
            'telefono': '44227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '44227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '44227654321')
    
    def test_max_length_en_telefono_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '1'*18,
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '1'*18,
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '+5144227654321')
        
    def test_caracteres_en_telefono_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': 'a',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': 'a',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '+5144227654321')
        
    def test_parentesis_en_telefono_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '(511234567890)',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '(511234567890)',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '+5144227654321')
    
    def test_espacios_en_telefono_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '442 2 123 123 1',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '442 2 123 123 1',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).telefono, '+5144227654321')
    
    def test_cambio_correo_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'este@mail.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'este@mail.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'este@mail.com')
    
    def test_no_correo_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'florentinop@realmadrid.com')
        
    def test_con_doble_dominio_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo@itesm.com.mx',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo@itesm.com.mx',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'ejemplo@itesm.com.mx')
        
    def test_con_mayusculas_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'Ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'Ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'Ejemplo@ejemplo.com')
        
    def test_correo_empieza_con_punto_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'florentinop@realmadrid.com')
    
    def test_correo_con_punto_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'ejemplo.ejemplo@ejemplo.com')
    
    def test_max_length_en_correo_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': ('a'*128)+'@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': ('a'*128)+'@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'florentinop@realmadrid.com')
    
    def test_correo_con_numeros_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'gods42@answere.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'gods42@answere.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).correo, 'gods42@answere.com')
    
    def test_cambio_color_local_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '3',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '3',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 3)
    
    def test_no_color_local_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 1)
    
    def test_color_local_negativo_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '-1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '-1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 1)
    
    def test_color_local_cero_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '0',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '0',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 1)
    
    def test_color_local_mayor_de_once_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '12',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '12',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 1)
    
    def test_color_local_letras_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': 'a',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': 'a',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 1)
    
    def test_color_local_caracteres_especiales_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '$',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '$',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorLocal, 1)
        
    def test_cambio_color_visitante_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '5',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '5',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 5)
    
    def test_no_color_visitante_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 2)
    
    def test_color_visitante_negativo_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '-2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '-2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 2)
    
    def test_color_visitante_cero_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '0',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '0',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 2)
    
    def test_color_visitante_mayor_de_once_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '2',
            'colorVisitante': '12',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '12',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 2)
    
    def test_color_visitante_letras_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': 'a',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': 'a',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 2)
    
    def test_color_visitante_caracteres_especiales_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '$',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '$',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).colorVisitante, 2)
    
    def test_cambio_cancha_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Estadio Azteca',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Estadio Azteca',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).cancha, 'Estadio Azteca')
    
    def test_no_cancha_en_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).cancha, 'Santiago Bernabéu')
    
    def test_numeros_en_cancha_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '1234',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '1234',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).cancha, '1234')
    
    def test_max_length_en_cancha_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'a'*129,
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'a'*129,
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).cancha, 'Santiago Bernabéu')
        
    def test_caracteres_especiales_en_cancha_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '%#<>$%^&*.,/\\""()(&$!',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '%#<>$%^&*.,/\\""()(&$!',
            'dia': '7',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).cancha, '%#<>$%^&*.,/\\""()(&$!')
    
    def test_cambio_dia_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '5',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '5',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 5)
    
    def test_no_dia_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 7)
    
    def test_dia_negativo_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '-1',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '-1',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 7)
    
    def test_dia_cero_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '1',
            'cancha': 'Santiago Bernabéu',
            'dia': '0',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '0',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 7)
    
    def test_dia_mayor_de_siete_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '8',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '8',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 7)
    
    def test_dia_letras_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': 'a',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': 'a',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 7)
    
    def test_dia_caracteres_especiales_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).dia, 7)
    
    def test_cambio_logo_equipo(self):
        team = self.equipo1()
        img = Equipo.objects.get(id = 1).logo
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '5',
            'hora': '13:05',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertNotEqual(Equipo.objects.get(id = 1).logo, img)
        
    def test_no_logo_equipo(self):
        team = self.equipo1()
        logo = Equipo.objects.get(id = 1).logo
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        file_data = {
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:05'
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(Equipo.objects.get(id = 1).logo, logo)
    
    def test_cambio_hora_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '11:11'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '11:11',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '11:11')
    
    
    def test_no_hora_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': ''
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
        
    def test_hora_negativa_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '-12:04'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '-12:04',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
    
    def test_letras_en_hora_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': 'once am'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': 'once am',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
    
    def test_formato_doce_horas_hora_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '10:54 am'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '10:54 am',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
    
    def test_horas_mayor_veinticuatro_hora_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '27:12'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '27:12',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
    
    def test_minutos_mayor_a_59_casoA_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:60'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:60',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
    
    def test_minutos_mayor_a_59_casoB_equipo(self):
        team = self.equipo1()
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:61'
        }
        file_data = {
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'hora': '13:61',
            'logo': SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        }
        form = equipoForm(form_data, file_data, team)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:editar_equipo', kwargs={'pk':1}), data)
        self.assertEqual(str(Equipo.objects.get(id = 1).hora.hour)+':'+str(Equipo.objects.get(id = 1).hora.minute), '13:18')
    
class TestEliminarEquipo(TestCase):
    
    def setUp(self):
        imagen = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
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
            logo = imagen,
            hora = '13:00'
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
            logo = imagen,
            hora = '13:00'
        )
    
    def tearDown(self):
        Equipo.objects.all().delete()
    
    def test_eliminar_equipo(self):
        response = self.client.get('/equipo/1/')
        self.assertEqual(response.status_code, 200)
        Equipo.objects.all().delete()
        response = self.client.get('/equipo/1/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Equipo.objects.count(),0)
    
    def test_vista_equipo(self):
        response = self.client.get('/equipo/borrar_equipo/2/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('equipo:borrar_equipo', kwargs={'pk':2}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/equipo/borrar_equipo/2/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/equipo/2/')
        self.assertEqual(response.status_code, 404)
   

    
