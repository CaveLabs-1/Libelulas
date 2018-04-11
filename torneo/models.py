from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from equipo.models import Equipo
from jugadora.models import Jugadora
import sys, os
import uuid

class Torneo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Torneo")
    categoria = models.IntegerField(verbose_name="Categoria", validators=[MaxValueValidator(datetime.datetime.now().year )])
    fechaInicio = models.DateField(verbose_name="Fecha Inicio")
    anexo = models.FileField(upload_to='media/torneo', blank=True, null=True, verbose_name="Documento Anexo")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Inscripcion", validators=[MinValueValidator(0)])
    costoCredencial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Credencial", validators=[MinValueValidator(0)])
    equipos = models.ManyToManyField(Equipo ,through='Estadisticas')
    activo = models.BooleanField(default = True)
    fechaJunta = models.DateField(verbose_name="Fecha de la siguiente junta")

    def delete(self):
        if self.anexo:
            if os.path.isfile(self.anexo.path):
                os.remove(self.anexo.path)
        super().delete()

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
    notas = models.CharField(max_length=100, blank=True)
    arbitro = models.CharField(max_length=50, blank=True)
    fecha = models.DateField(verbose_name="Fecha Partido")
    hora = models.TimeField(verbose_name='Hora de Juego')
    cancha = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.id)

class Tarjetas_amarillas(models.Model):
    partido = models.ForeignKey(Partido, on_delete = models.CASCADE)
    jugadora = models.ForeignKey(Jugadora, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 0)

class Tarjetas_rojas(models.Model):
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
