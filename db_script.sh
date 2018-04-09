#!/bin/bash



echo ''
echo 'Ejecutando script de generacion de base de datos'
> database.sql
echo ''
echo 'Borrado de base de datos'
echo ''
echo 'drop database libelulas;' >> database.sql
echo ''
echo 'Creacion de base de datos'
echo ''
echo 'create database libelulas;' >> database.sql


psql  < "database.sql"

rm ./database.sql
echo ''
echo 'Borrado de migraciones'
echo ''

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
echo ''
echo 'Borrado de creación de migraciones'
echo ''

python manage.py makemigrations torneo
python manage.py makemigrations jugadora
python manage.py makemigrations landing
python manage.py makemigrations equipo

echo ''
echo 'Ejecutando de migraciones '
echo ''


python manage.py migrate


echo ''
echo '>>>>>>Creacion de superusuario U:libelulas  P:0123456abc '
echo ''


./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('libelulas', 'libelulas@example.com', '0123456abc')"

echo ''
echo 'creacion Jugadora'
echo ''


./manage.py shell -c "
from django.db import models;
from jugadora.models import Jugadora;
from equipo.models import Equipo;
from django.core.files.uploadedfile import SimpleUploadedFile;

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


b = Jugadora.objects.create(
    Nombre = 'Nombre B',
    Apellido = 'Apellido B',
    Nacimiento = '1997-02-01',
    Numero = 2,
    Posicion = 2,
    Notas = 'Ejemplo B Jugadora',
    Imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora2.jpg', 'rb').read(), content_type='image/jpeg')

);
b.save();


c = Jugadora.objects.create(
    Nombre = 'Nombre C',
    Apellido = 'Apellido C',
    Nacimiento = '1997-03-01',
    Numero = 3,
    Posicion = 3,
    Notas = 'Ejemplo C Jugadora',
    Imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora3.jpg', 'rb').read(), content_type='image/jpeg')

);
c.save();


c = Jugadora.objects.create(
    Nombre = 'Nombre C',
    Apellido = 'Apellido C',
    Nacimiento = '1997-03-01',
    Numero = 3,
    Posicion = 3,
    Notas = 'Ejemplo C Jugadora',
    Imagen =  SimpleUploadedFile(name='test_image.jpg', content=open(sys.path[0]+'/static/static_media/jugadora3.jpg', 'rb').read(), content_type='image/jpeg')

);
c.save();


d = Jugadora.objects.create(
    Nombre = 'Nombre Def',
    Apellido = 'Apellido Def',
    Nacimiento = '1998-03-01',
    Numero = 4,
    Posicion = 1,
    Notas = 'Ejemplo Default Jugadora',
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









"


echo ''
echo 'Corriendo servidor ...'
echo ''

python manage.py runserver
