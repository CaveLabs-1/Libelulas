from django.forms import ModelForm
from .models import Torneo
from django.forms.widgets import FileInput
from django import forms
from equipo.models import Equipo

class torneoForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super(torneoForm, self).__init__(*args, **kwargs)
        self.fields['anexo'].widget.attrs['class'] = 'inputfile'
        self.fields['anexo'].widget.attrs['onchange'] = 'loadFile(event)'

    class Meta:
        model = Torneo
        fields = ( 'nombre','categoria', 'fechaInicio', 'anexo','costo', 'equipos')
        widgets = {
            'anexo': forms.FileInput(),
        }


