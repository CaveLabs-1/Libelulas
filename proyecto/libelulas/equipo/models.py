from django.db import models

# Create your models here.
from django.core.validators import RegexValidator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.

class Equipo(models.Model):
    nombre = models.CharField(
        max_length=64, 
        unique=True, 
        default='', 
        verbose_name='Nombre')
    representante = models.CharField(
        max_length=64, 
        default='', 
        verbose_name='Representante')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="El numero de telefono debe estar en este formato: '+999999999'. Con 15 digitos maximos permitidos.")
    telefono = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        default='', 
        verbose_name='Telefono')
    correo = models.EmailField(
        max_length=128, 
        default='', 
        verbose_name='Correo Electronico' )
    logo = models.ImageField(
        upload_to='media/equipo',
        default='',
        verbose_name='Logo')
    COLORES = (
        (1, 'Blanco'),
        (2, 'Gris'),
        (3, 'Negro'),
        (4, 'Rojo'),
        (5, 'Naranja'),
        (6, 'Amarillo'),
        (7, 'Verde'),
        (8, 'Azul'),
        (9, 'Morado'),
        (10, 'Rosa'),
        (11, 'Cafe'),
    )
    colorLocal  = models.IntegerField(
        choices=COLORES,
        default=1, 
        verbose_name='Color de Local')
    colorVisitante = models.IntegerField(
        choices=COLORES,
        default=1,
        verbose_name='Color de Visitante')
    cancha = models.CharField(
        max_length=128, 
        default='', 
        verbose_name='Cancha del Equipo')
    DIAS_DE_JUEGO = (
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miercoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sabado'),
        (7, 'Domingo'),
    )
    dia = models.IntegerField(
        choices=DIAS_DE_JUEGO,
        default=1,
        verbose_name='Dia de Juego')
    hora = models.TimeField(
        verbose_name='Hora de Juego',
        )
        

    def __str__(self):
        return self.Nombre

    def save(self):
        # Opening the uploaded image
        im = Image.open(self.Imagen)

        output = BytesIO()


        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=70)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.Logo = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.Imagen.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Equipo, self).save()