from django.db import models
from jugadora.models import Jugadora

# Create your models here.
from django.core.validators import RegexValidator
from PIL import Image
from PIL import ImageDraw
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys, os
from django.dispatch import receiver


# Create your models here.

class Equipo(models.Model):
    jugadoras = models.ManyToManyField(Jugadora)
    nombre = models.CharField(
        max_length=64,
        unique=True,
        default='',
        verbose_name='Nombre')
    repre_regex = RegexValidator(
        regex=r'[a-zA-ZéíóúáäöüßÄÖÜÁÉÍÓÚñÑ\s]+$',
        message="El representante debe de ")
    representante = models.CharField(
        validators=[repre_regex],
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
        verbose_name='Teléfono')
    correo = models.EmailField(
        max_length=128,
        default='',
        verbose_name='Correo Electronico' )
    logo = models.ImageField(
        upload_to='media/equipo',
        blank=True,
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
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miercoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sabado'),
        (6, 'Domingo'),
    )
    dia = models.IntegerField(
        choices=DIAS_DE_JUEGO,
        default=1,
        verbose_name='Dia de Juego')
    hora = models.TimeField(
        verbose_name='Hora de Juego',
        )
    activo = models.BooleanField(default = True)


    def __str__(self):
        return self.nombre

    def delete(self):
        if self.logo:
            if os.path.isfile(self.logo.path):
                os.remove(self.logo.path)
        super().delete()

    def save(self, *args, **kw):

        if self.logo:
            try:


                # Opening the uploaded image

                im = Image.open(self.logo)

                nombre = (self.logo.name)

                if im.mode in ('RGBA', 'LA'):
                    background = Image.new(im.mode[:-1], im.size, 0)
                    background.paste(im, im.split()[-1])
                    im = background


                output = BytesIO()



                # after modifications, save it to the output
                im.save(output, format='JPEG', quality=70)
                output.seek(0)

                # change the imagefield value to be the newley modifed image value
                self.logo = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.logo.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            except:
                print("gg")
        super(Equipo,self).save(*args, **kw)
