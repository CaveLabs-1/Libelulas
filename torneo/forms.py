from django.forms import *
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
        fields = ('nombre', 'categoria', 'categoriaMax', 'fechaInicio', 'anexo', 'costo', 'costoCredencial', 'equipos', 'fechaJunta')
        widgets = {
            'anexo': forms.FileInput(),
        }

class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = (
            'fecha',
            'hora',
            'cancha',
        )

class CedulaForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ('goles_local', 'goles_visitante', 'notas', 'arbitro')

class JornadaForm(forms.ModelForm):
    class Meta:
        model = Jornada
        fields = ('fecha_inicio', 'fecha_fin', 'jornada')
        
class NuevoPartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = (
            'fecha',
            'hora',
            'cancha',
            'equipo_local',
            'equipo_visitante',
        )
class GanadorForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.fields['equipos'].widget.attrs['class'] = 'select'
    
    class Meta:
        model= Torneo
        fields = (
            'equipos',
        )
        widgets = {
            'equipos': forms.Select(),
        }
        