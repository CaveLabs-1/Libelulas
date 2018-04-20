from django.contrib import admin
from torneo.models import *
admin.site.register(Torneo)
admin.site.register(Partido)
admin.site.register(Estadisticas)
admin.site.register(Jornada)
admin.site.register(Asistencia)
admin.site.register(Goles)
admin.site.register(TarjetasAmarillas)
admin.site.register(TarjetasRojas)
admin.site.register(Tarjetas_azules)

