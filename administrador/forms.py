from django import forms
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')

    def clean_email(self):

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("Este email ya se encuentra en uso.")

        try:
            validate_email(self.cleaned_data['email'])
            return self.cleaned_data['email']
        except ValidationError:
            raise forms.ValidationError("Este email no es válido.")

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def clean_email(self):

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("Este email ya se encuentra en uso.")

        try:
            validate_email(self.cleaned_data['email'])
            return self.cleaned_data['email']
        except django.core.exceptions.ValidationError:
            raise forms.ValidationError("Este email no es válido.")

class UpdatePasswordForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password',)

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
