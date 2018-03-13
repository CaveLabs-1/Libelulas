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

# Create your tests here.
class TestCrearEquipo(TestCase):

    def test_happy_crear_equipo(self):
        #Revisar que no hay equipos
        self.assertEqual(Equipo.objects.count(), 0)
        #Hacer un update de una imagen correcta
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
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
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
        #Pruebo que se vea el equipo despues de creado
        pk = Equipo.objects.get(nombre='Real Madrid Futboll Club').id
        response = self.client.get('/equipo/'+str(pk)+'/')
        self.assertEqual(response.status_code, 200)
    
    def test_no_nombre_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': '',
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
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_numeros_en_nombre_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': '123',
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
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_nombre_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'a'*65,
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
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_especiales_en_nombre_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': '%#<>$%^&*.,/\\""()(&$!',
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
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_representante_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_numeros_en_representate_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
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
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_max_length_en_representante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C', 
            'representante': 'a'*65,
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_especiales_en_representante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': '%#$%^&*""()(&$!',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_acentos_en_representante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'éáíóúüñÉÍÁÓÚ',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
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
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_sin_extencion_de_pais_numero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C',
            'representante': 'Florentino Pérez',
            'telefono': '44227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '1'*18,
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': 'a',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_parentesis_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '(511234567890)',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_espacios_en_telefono_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '442 2 123 123 1',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_correo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_con_doble_dominio_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo@itesm.com.mx',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
        
    def test_con_mayusculas_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'Ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
        
    def test_correo_empieza_con_punto_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': '.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_correo_con_punto_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'ejemplo.ejemplo@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_correo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': ('a'*128)+'@ejemplo.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_correo_con_numeros_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'gods42@answere.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_color_local_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_negativo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '-1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_cero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '0',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_mayor_de_once_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '12',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_letras_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': 'a',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_local_caracteres_especiales_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '$',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_no_color_visitante_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_negativo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '-2',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_cero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '0',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_mayor_de_once_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '2',
            'colorVisitante': '12',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_letras_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': 'a',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_color_visitante_caracteres_especiales_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '$',
            'cancha': 'Santiago Bernabéu',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_cancha_en_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_numeros_en_cancha_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': '123',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '1234',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_max_length_en_cancha_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'a'*129,
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_caracteres_especiales_en_cancha_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': '%#<>$%^&*.,/\\""()(&$!',
            'dia': '7',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertTrue(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 1)
    
    def test_no_dia_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_negativo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '-1',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_cero_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '1',
            'cancha': 'Santiago Bernabéu',
            'dia': '0',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_mayor_de_siete_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '8',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_letras_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': 'a',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_dia_caracteres_especiales_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_logo_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': '',
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_logo_not_imgfile_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.txt', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='text/plain')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_logo_double_file_type_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.txt.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '13:05'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_no_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': ''
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_hora_negativa_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '-12:04'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_letras_en_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': 'once am'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_formato_segundos_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '13:01:54'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
        
    def test_formato_doce_horas_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '10:54 am'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_horas_mayor_veinticuatro_hora_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '27:12'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_minutos_mayor_a_59_casoA_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '13:60'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    
    def test_minutos_mayor_a_59_casoB_equipo(self):
        self.assertEqual(Equipo.objects.count(), 0)
        logo = SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/default.jpg', 'rb').read(), content_type='image/jpeg')
        form_data = {
            'nombre': 'Real Madrid F.C.',
            'representante': 'Florentino Pérez',
            'telefono': '+5144227654321',
            'correo': 'florentinop@realmadrid.com',
            'colorLocal': '1',
            'colorVisitante': '2',
            'cancha': 'Santiago Bernabéu',
            'dia': '%',
            'logo': logo,
            'hora': '13:61'
        }
        form = equipoForm(data=form_data)
        #Pruebo que la forma sea correcta
        self.assertFalse(form.is_valid())
        #Pruebo que se guarde el equipo
        self.client.post(reverse('equipo:agregar_equipo'), form_data)
        self.assertEqual(Equipo.objects.count(), 0)
    