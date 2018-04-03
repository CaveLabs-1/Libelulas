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
echo 'Corriendo servidor ...'
echo ''

python manage.py runserver