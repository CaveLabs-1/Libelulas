# Generated by Django 2.0.2 on 2018-03-05 18:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=64, unique=True, verbose_name='Nombre')),
                ('representante', models.CharField(default='', max_length=64, verbose_name='Representante')),
                ('telefono', models.CharField(default='', max_length=17, validators=[django.core.validators.RegexValidator(message="El numero de telefono debe estar en este formato: '+999999999'. Con 15 digitos maximos permitidos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Teléfono')),
                ('correo', models.EmailField(default='', max_length=128, verbose_name='Correo Electronico')),
                ('logo', models.ImageField(default='', upload_to='media/equipo', verbose_name='Logo')),
                ('colorLocal', models.IntegerField(choices=[(1, 'Blanco'), (2, 'Gris'), (3, 'Negro'), (4, 'Rojo'), (5, 'Naranja'), (6, 'Amarillo'), (7, 'Verde'), (8, 'Azul'), (9, 'Morado'), (10, 'Rosa'), (11, 'Cafe')], default=1, verbose_name='Color de Local')),
                ('colorVisitante', models.IntegerField(choices=[(1, 'Blanco'), (2, 'Gris'), (3, 'Negro'), (4, 'Rojo'), (5, 'Naranja'), (6, 'Amarillo'), (7, 'Verde'), (8, 'Azul'), (9, 'Morado'), (10, 'Rosa'), (11, 'Cafe')], default=1, verbose_name='Color de Visitante')),
                ('cancha', models.CharField(default='', max_length=128, verbose_name='Cancha del Equipo')),
                ('dia', models.IntegerField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sabado'), (7, 'Domingo')], default=1, verbose_name='Dia de Juego')),
                ('hora', models.TimeField(verbose_name='Hora de Juego')),
            ],
        ),
    ]
