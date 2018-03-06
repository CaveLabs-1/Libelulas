from django.forms import ModelForm
from .models import Jugadora
from django.forms.widgets import FileInput
from django import forms

class jugadoraForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(jugadoraForm, self).__init__(*args, **kwargs)
        self.fields['Imagen'].widget.attrs['class'] = 'inputfile'
        self.fields['Nacimiento'].widget.input_type = 'date'
        self.fields['Numero'].widget.attrs['min'] = '0'
        self.fields['Imagen'].widget.attrs['onchange'] = 'loadFile(event)'

    class Meta:
        model = Jugadora
        fields = ('Nombre', 'Apellido', 'Nacimiento', 'Numero', 'Posicion', 'Notas', 'Imagen')
        widgets = {
            'Imagen': forms.FileInput(),
        }
