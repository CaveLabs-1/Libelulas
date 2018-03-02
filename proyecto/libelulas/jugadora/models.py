from django.db import models
from sorl.thumbnail import ImageField

# Create your models here.

class Jugadora(models.Model):
    Nombre = models.CharField(max_length=50, default='', verbose_name='Nombre')
    Apellido = models.CharField(max_length=50, default='', verbose_name='Apellido')
    Nacimiento = models.DateField(default='', verbose_name='Fecha de Nacimiento')
    Numero = models.IntegerField(default='', verbose_name='Número')
    Posicion = models.IntegerField(default='', verbose_name='Posición')
    Notas = models.TextField(max_length=150, default='', verbose_name='Comentarios')
    Imagen = ImageField(upload_to='media/jugadora' , default='', verbose_name='Foto')

    def __str__(self):
        return self.Nombre
