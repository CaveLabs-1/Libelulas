from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator
import sys
import os
import datetime

# Create your models here.

class Jugadora(models.Model):
    POSICION = (
        (1, 'Delantero'),
        (2, 'Medio'),
        (3, 'Defensa'),
        (4, 'Portero'),
    )
    nombre = models.CharField(max_length=50, default='', verbose_name='Nombre')
    apellido = models.CharField(max_length=50, default='', verbose_name='Apellido')
    nacimiento = models.DateField(default='', verbose_name='Fecha de Nacimiento')
    numero = models.IntegerField(default='', verbose_name='Número de playera', validators=[MinValueValidator(0), MaxValueValidator(1000)])
    posicion = models.IntegerField(default='', choices=POSICION, verbose_name='Posición')
    notas = models.TextField(max_length=150, default='', verbose_name='Comentarios', null=True, blank=True)
    imagen = models.ImageField(upload_to='jugadora', verbose_name='Foto', null=True, blank=True)
    fecha_de_afiliacion = models.DateField(default='', verbose_name='Fecha de Afiliacón')
    num_poliza  = models.CharField(max_length=50, default='', verbose_name='Numero de Póliza', null=True, blank=True)
    nui = models.CharField(max_length=50, default='', verbose_name='NUI', null=True, blank=True)
    activo = models.BooleanField(default = True)

    def __str__(self):
        return self.nombre + str(self.pk)

    def save(self, *args, **kw):
        
        if self.imagen:
            try:
                # Opening the uploaded image
                im = Image.open(self.imagen)
    
                nombre = (self.imagen.name)
                fill_color = ''
                if im.mode in ('RGBA', 'LA'):
                    background = Image.new(im.mode[:-1], im.size, 0)
                    background.paste(im, im.split()[-1])
                    im = background
    
    
                output = BytesIO()
    
    
                # after modifications, save it to the output
                im.save(output, format='JPEG', quality=70)
                output.seek(0)
    
                # change the imagefield value to be the newley modifed image value
                self.imagen = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.Imagen.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            except:
                print("gg")
        self.fecha_de_afiliacion = datetime.date.today()
        super(Jugadora,self).save(*args, **kw)
    

    def delete(self):
        if self.imagen:
            if os.path.isfile(self.imagen.path):
                os.remove(self.imagen.path)
        super().delete()
