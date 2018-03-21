from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from equipo.models import Equipo
from jugadora.models import Jugadora
import sys, os
import uuid


class Torneo(models.Model):
    nombre=models.CharField(max_length=100, verbose_name="Nombre del Torneo")
    categoria=models.IntegerField(verbose_name="Categoria", validators=[MaxValueValidator(datetime.datetime.now().year )])
    fechaInicio=models.DateField(verbose_name="Fecha Inicio")
    anexo=models.FileField(upload_to='media/torneo', blank=True, null=True, verbose_name="Documento Anexo")
    costo=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Inscripcion", validators=[MinValueValidator(0)])
    costoCredencial=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Credencial", validators=[MinValueValidator(0)])
    equipos=models.ManyToManyField(Equipo, blank=True)
    activo=models.BooleanField(default = True)

    fechaJunta = models.DateField(verbose_name="Fecha de la siguiente junta")
    def delete(self):
        if self.anexo:
            if os.path.isfile(self.anexo.path):
                os.remove(self.anexo.path)
        super().delete()

class Partido(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex[:6].upper(), editable=False, max_length=6)
    torneo = models.ForeignKey(Torneo, on_delete = models.CASCADE)
    equipo_local =  models.ForeignKey(Equipo, on_delete = models.CASCADE, related_name='equipo_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete = models.CASCADE, related_name='equipo_visitante')
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    notas = models.CharField(max_length=100, blank=True)
    arbitro = models.CharField(max_length=50)
    fecha = models.DateField(verbose_name="Fecha Partido")
    hora = models.TimeField(verbose_name='Hora de Juego')

class Tarjetas_amarillas(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 0)

class Tarjetas_rojas(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    directa = models.BooleanField(default = False)

class Tarjetas_azules(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)

class Goles(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 0)

class Asistencia(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
