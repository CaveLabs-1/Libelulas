from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from equipo.models import Equipo
import sys, os


class Torneo(models.Model):


    nombre=models.CharField(max_length=100, verbose_name="Nombre del Torneo")
    categoria=models.IntegerField(verbose_name="Categoria", validators=[MaxValueValidator(datetime.datetime.now().year )])
    fechaInicio=models.DateField(verbose_name="Fecha Inicio")
    anexo=models.FileField(upload_to='media/torneo', blank=True, null=True, verbose_name="Documento Anexo")
    costo=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Inscripcion", validators=[MinValueValidator(0)])
    costoCredencial=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Credencial", validators=[MinValueValidator(0)])
    equipos=models.ManyToManyField(Equipo, blank=True)
    fechaJunta = models.DateField(verbose_name="Fecha Inicio")
    
    def delete(self):
        if self.anexo:
            if os.path.isfile(self.anexo.path):
                os.remove(self.anexo.path)
        super().delete()