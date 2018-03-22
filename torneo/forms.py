from django.forms import ModelForm
from .models import *
from django.forms.widgets import FileInput
from django import forms
from equipo.models import Equipo

class torneoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(torneoForm, self).__init__(*args, **kwargs)
        self.fields['anexo'].widget.attrs['class'] = 'inputfile'
        self.fields['anexo'].widget.attrs['onchange'] = 'loadFile(event)'
        self.fields['fechaInicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fechaInicio'].widget.input_type = 'date'
        self.fields['fechaJunta'].widget.attrs['class'] = 'datepicker'
        self.fields['fechaJunta'].widget.input_type = 'date'

    class Meta:
        model = Torneo
        fields = ('nombre', 'categoria', 'fechaInicio', 'anexo', 'costo', 'costoCredencial', 'equipos', 'fechaJunta')
        widgets = {
            'anexo': forms.FileInput(),
        }

class PartidoForm(ModelForm):
    class Meta:
        model = Partido
        fields = ['goles_local', 'goles_visitante', 'notas', 'arbitro', 'fecha', 'hora', 'cancha']

class TarjetaAmarillaForm(ModelForm):
    class Meta:
        model = Tarjetas_amarillas
        fields = ['partido', 'jugadora', 'cantidad']

class TarjetaRojaForm(ModelForm):
    class Meta:
        model = Tarjetas_rojas
        fields = ['partido', 'jugadora', 'directa']

class TarjetaAzulForm(ModelForm):
    class Meta:
        model = Tarjetas_azules
        fields = ['partido', 'jugadora']
