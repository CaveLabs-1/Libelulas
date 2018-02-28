from django.forms import ModelForm
from .models import Jugadora

class jugadoraForm(ModelForm):
    class Meta:
        model = Jugadora
        fields = ('Nombre', 'Apellido', 'Nacimiento', 'Numero', 'Posicion', 'Notas', 'Imagen')
