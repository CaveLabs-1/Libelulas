from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from equipo.models import Equipo



class Torneo(models.Model):


    nombre=models.CharField(max_length=100, verbose_name="Nombre del Torneo")
    categoria=models.IntegerField(verbose_name="Categoria", validators=[MaxValueValidator(datetime.datetime.now().year )])
    fechaInicio=models.DateField(verbose_name="Fecha Inicio")
    anexo=models.FileField(upload_to='media/torneo', blank=True, null=True, verbose_name="Documento Anexo")
    costo=models.IntegerField(verbose_name="Costo", validators=[MinValueValidator(0)])
    equipos=models.ManyToManyField(Equipo)
