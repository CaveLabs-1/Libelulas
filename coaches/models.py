from django.db import models
from torneo.models import Torneo

class PreRegistro(models.Model):
    Nombre = models.CharField(max_length=50, default='', verbose_name='Nombre')
    Correo = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    Notas = models.CharField(max_length=50, default='', verbose_name='Notas')
    codigo = models.CharField(max_length=16, null=True, blank=True)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, null=True)
