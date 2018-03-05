from django.db import models

# Create your models here.
from django.core.validators import RegexValidator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.

class Equipo(models.Model):
    Nombre = models.CharField(
        max_length=64, 
        unique=True, 
        default='', 
        verbose_name='Nombre')
    Representante = models.CharField(
        max_length=64, 
        default='', 
        verbose_name='Representante')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="El numero de telefono debe estar en este formato: '+999999999'. Con 15 digitos maximos permitidos.")
    Telefono = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        default='', 
        verbose_name='Telefono')
    Correo = models.EmailField(
        max_length=128, 
        default='', 
        verbose_name='Correo Electronico' )
    Logo = models.ImageField(
        upload_to='media/equipo',
        default='',
        verbose_name='Logo')
    ColorVisitante = models.CharField(
        max_length=7,
        default='',
        verbose_name='Color de Visitante')
    ColorLocal  = models.CharField(
        max_length=7, 
        default='', 
        verbose_name='Color de Local')
    Cancha = models.CharField(
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
    Dia = models.IntegerField(
        choices=DIAS_DE_JUEGO,
        default=1)
    Hora = models.TimeField()
        

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