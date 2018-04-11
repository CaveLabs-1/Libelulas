from django.db import models
from torneo.models import Torneo
from equipo.models import *

class PreRegistro(models.Model):
    nombre = models.CharField(max_length=50, default='', verbose_name='Nombre')
    correo = models.EmailField(max_length=50, blank=False, null=False)
    notas = models.CharField(max_length=50, default='', verbose_name='Notas')
    codigo = models.CharField(max_length=16, null=True, unique=True)
    torneo = models.ForeignKey(Torneo, on_delete = models.CASCADE, null=True)
    equipo = models.ForeignKey(Equipo, on_delete = models.CASCADE, null=True)
