from django import forms
from .models import PreRegistro

class PreForm(forms.ModelForm):

    class Meta:
        model = PreRegistro
        fields = ('Nombre', 'Correo', 'Notas')
