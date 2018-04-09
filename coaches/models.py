from django.db import models

class PreRegistro(models.Model):
    Nombre = models.CharField(max_length=50, default='', verbose_name='Nombre')
    Correo = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    Notas = models.CharField(max_length=50, default='', verbose_name='Nombre')
    codigo = models.CharField(max_length=16)
