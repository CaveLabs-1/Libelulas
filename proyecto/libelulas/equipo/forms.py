from django.forms import ModelForm
from .models import Equipo

class equipoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(equipoForm, self).__init__(*args, **kwargs)
        self.fields['logo'].widget.attrs['class'] = 'inputfile'
        self.fields['hora'].widget.input_type = 'time'
        self.fields['logo'].widget.attrs['onchange'] = 'loadFile(event)'

    class Meta:
        model = Equipo
        fields = (
            'nombre',
            'representante',
            'telefono',
            'correo',
            'logo',
            'colorLocal',
            'colorVisitante',
            'cancha',
            'dia',
            'hora'
        )

