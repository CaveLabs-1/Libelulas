from django.forms import ModelForm
from .models import Jugadora
from django.forms.widgets import FileInput
from django import forms
from equipo.models import Equipo

class jugadoraForm(ModelForm):

    equipo = forms.ModelChoiceField(queryset=Equipo.objects.all(), empty_label="Elige un Equipo")

    def __init__(self, *args, **kwargs):
        super(jugadoraForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs['class'] = 'inputfile'
        self.fields['nacimiento'].widget.input_type = 'date'
        self.fields['numero'].widget.attrs['min'] = '0'
        self.fields['numero'].widget.attrs['max'] = '1000'
        self.fields['imagen'].widget.attrs['onchange'] = 'loadFile(event)'
        self.fields['equipo'].required = False
        self.fields['nacimiento'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_de_afiliacion'].widget.input_type = 'date'



    class Meta:
        model = Jugadora
        fields = ('nombre', 'apellido', 'nacimiento', 'fecha_de_afiliacion', 'numero', 'posicion', 'num_poliza', 'nui', 'notas', 'imagen')
        widgets = {
            'imagen': forms.FileInput(),
        }

class jugadoraEquipoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(jugadoraEquipoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs['class'] = 'inputfile'
        self.fields['nacimiento'].widget.input_type = 'date'
        self.fields['numero'].widget.attrs['min'] = '0'
        self.fields['numero'].widget.attrs['max'] = '1000'
        self.fields['imagen'].widget.attrs['onchange'] = 'loadFile(event)'
        self.fields['nacimiento'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_de_afiliacion'].widget.attrs['class'] = 'datepicker'

    class Meta:
        model = Jugadora
        fields = ('nombre', 'apellido', 'nacimiento', 'fecha_de_afiliacion' , 'numero', 'posicion', 'num_poliza', 'nui', 'notas', 'imagen')
        widgets = {
            'imagen': forms.FileInput(),
        }
