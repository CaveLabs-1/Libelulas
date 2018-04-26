#!/bin/bash



find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
echo ''
echo 'Borrado de creación de migraciones'
echo ''

python3 manage.py makemigrations torneo
python3 manage.py makemigrations jugadora
python3 manage.py makemigrations landing
python3 manage.py makemigrations equipo
python3 manage.py makemigrations coaches

echo ''
echo 'Ejecutando de migraciones '
echo ''


python3 manage.py migrate


echo ''
echo '>>>>>>Creacion de superusuario U:libelulas  P:0123456abc '
echo ''


python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('libelulas', 'libelulas@example.com', '0123456abc')"

echo ''
echo 'creacion Jugadora'
echo ''


python3 manage.py shell -c "
from django.db import models;
from jugadora.models import Jugadora;
from equipo.models import Equipo;
from django.core.files.uploadedfile import SimpleUploadedFile;

a = Jugadora.objects.create(
    nombre = 'Nombre A',
    apellido = 'Apellido A',
    nacimiento = '1997-01-01',
    numero = 1,
    posicion = 1,
    notas = 'Ejemplo A Jugadora',
    imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora1.jpg', 'rb').read(), content_type='image/jpeg'),
    fecha_de_afiliacion = '2000-01-01',
    num_poliza  = "5533535",
    nui = "39329924924",
    activo = True,


);
a.save();


b = Jugadora.objects.create(
    nombre = 'Nombre B',
    apellido = 'Apellido B',
    nacimiento = '1997-02-01',
    numero = 12,
    posicion = 2,
    notas = 'Ejemplo B Jugadora',
    imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora2.jpg', 'rb').read(), content_type='image/jpeg'),
    fecha_de_afiliacion = '2001-01-01',
    num_poliza  = "5533535",
    nui = "33334546457",
    activo = True,


);
b.save();


c = Jugadora.objects.create(
    nombre = 'Nombre C',
    apellido = 'Apellido C',
    nacimiento = '1995-01-01',
    numero = 4,
    posicion = 1,
    notas = 'Ejemplo C Jugadora',
    imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora3.jpg', 'rb').read(), content_type='image/jpeg'),
    fecha_de_afiliacion = '2000-01-01',
    num_poliza  = "5533535",
    nui = "393299234924",
    activo = True,


);
c.save();


d = Jugadora.objects.create(
    nombre = 'Nombre Def',
    apellido = 'Apellido D',
    nacimiento = '1990-01-01',
    numero = 44,
    posicion = 1,
    notas = 'Ejemplo Def Jugadora',
    fecha_de_afiliacion = '2001-01-01',
    num_poliza  = "5533535",
    nui = "39329924924",
    activo = True,


);
d.save();


print ('creacion Equipos*********');

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
   hora = '13:05'
   )

ea.save();

ea.jugadoras.add(a,b)
ea.save();



eb = Equipo.objects.create(


   nombre = 'Equipo B',
   representante = 'Juan B',
   telefono = '4426483003',
   correo = 'rr100@live.com.mx',
   logo =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/balon2.jpg', 'rb').read(), content_type='image/jpeg'),
   colorLocal  = 4,
   colorVisitante = 6,
   cancha = 'Estadio B',
   dia = 3,
   hora = '18:05'
   )
eb.save();

eb.jugadoras.add(c)
eb.save();



ec = Equipo.objects.create(


   nombre = 'Equipo c',
   representante = 'Juan c',
   telefono = '4426483003',
   correo = 'rr100@live.com.mx',
   logo =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/balon3.jpg', 'rb').read(), content_type='image/jpeg'),
   colorLocal  = 6,
   colorVisitante = 5,
   cancha = 'Estadio C',
   dia = 4,
   hora = '15:05'
   )

ec.save();

ec.jugadoras.add(d)
ec.save();


ed = Equipo.objects.create(



   nombre = 'Equipo Def',
   representante = 'Juan De',
   telefono = '4426483003',
   correo = 'rr100@live.com.mx',
   logo =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/balon4.jpg', 'rb').read(), content_type='image/jpeg'),
   colorLocal  = 6,
   colorVisitante = 5,
   cancha = 'Estadio D',
   dia = 4,
   hora = '15:05'
   )

ed.save();

ed.jugadoras.add(d)
ed.save();









"


echo ''
echo 'Corriendo servidor ...'
echo ''

python3 manage.py runserver



