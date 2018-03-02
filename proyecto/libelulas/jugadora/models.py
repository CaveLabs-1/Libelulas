from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.

class Jugadora(models.Model):
    POSICION=(
        (1, 'Delantero'),
        (2, 'Medio'),
        (3, 'Defensa'),
        (4, 'Portero'),
    )

    Nombre = models.CharField(max_length=50, default='', verbose_name='Nombre')
    Apellido = models.CharField(max_length=50, default='', verbose_name='Apellido')
    Nacimiento = models.DateField(default='', verbose_name='Fecha de Nacimiento')
    Numero = models.IntegerField(default='', verbose_name='Número')
    Posicion = models.IntegerField(default='', choices=POSICION, verbose_name='Posición')
    Notas = models.TextField(max_length=150, default='', verbose_name='Comentarios')
    Imagen = models.ImageField(upload_to='media/jugadora' , default='', verbose_name='Foto')

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
        self.Imagen = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.Imagen.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Jugadora, self).save()



