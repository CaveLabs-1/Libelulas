from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from datetime import timedelta
from equipo.models import Equipo
from jugadora.models import Jugadora
import sys, os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator


class Torneo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Torneo")
    categoria = models.IntegerField(verbose_name="Edad (Años) desde:", default=0, validators=[ MaxValueValidator(100), MinValueValidator(0)])
    categoria_max = models.IntegerField(verbose_name="Edad (Años) hasta:", default=0,validators=[ MaxValueValidator(100),MinValueValidator(0)] )
    fecha_inicio = models.DateField(verbose_name="Fecha Inicio")
    anexo = models.FileField(upload_to='media/torneo', blank=True, null=True, verbose_name="Documento Anexo")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Inscripcion", validators=[MinValueValidator(0)])
    costo_credencial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Credencial", validators=[MinValueValidator(0)])
    equipos = models.ManyToManyField(Equipo ,blank=True ,through='Estadisticas')
    activo = models.BooleanField(default = True)
    ganador = models.BooleanField(default = False)
    fecha_junta = models.DateField(verbose_name="Fecha de la siguiente junta")

    #Eliminar el archivo anexo
    def delete(self):
        if self.anexo:
            if os.path.isfile(self.anexo.path):
                os.remove(self.anexo.path)
        super().delete()

    def unDiaAntesJunta(self):
        return self.fecha_junta - timedelta(days=1)

class Estadisticas(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete = models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete = models.CASCADE)
    jugados = models.IntegerField(verbose_name="Jugados", default=0)
    puntos = models.IntegerField(verbose_name="Puntos", default=0)
    ganados = models.IntegerField(verbose_name="Ganados", default=0)
    empatados = models.IntegerField(verbose_name="Empatados", default=0)
    perdidos = models.IntegerField(verbose_name="Perdidos", default=0)
    goles_favor = models.IntegerField(verbose_name="GF", default=0)
    goles_contra = models.IntegerField(verbose_name="GC", default=0)
    ganador = models.BooleanField(default=False)

class Jornada(models.Model):
    jornada = models.CharField(max_length=50)
    fecha_inicio = models.DateField(verbose_name="Fecha Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha Fin")
    torneo = models.ForeignKey(Torneo, on_delete = models.CASCADE)

    def __str__(self):
        return self.jornada

class Partido(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=6)
    jornada = models.ForeignKey(Jornada, on_delete = models.CASCADE)
    equipo_local =  models.ForeignKey(Equipo, on_delete = models.CASCADE, related_name='equipo_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete = models.CASCADE, related_name='equipo_visitante')
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    notas = models.CharField(max_length=500, blank=True)
    arbitro = models.CharField(max_length=500, blank=True)
    fecha = models.DateField(verbose_name="Fecha Partido")
    hora = models.TimeField(verbose_name='Hora de Juego')
    cancha = models.CharField(max_length=50, blank=True)
    registrado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class TarjetasAmarillas(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 0)

class TarjetasRojas(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    directa = models.BooleanField(default=False)

class Tarjetas_azules(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)

class Goles(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 0)

class Asistencia(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete = models.CASCADE)
