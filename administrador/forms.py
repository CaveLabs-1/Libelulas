from django import forms
from .models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("Este email ya se encuentra en uso.")
        return self.cleaned_data['email']

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']).exclude(pk=self.instance.pk):
            raise forms.ValidationError("Este email ya se encuentra en uso.")
        return self.cleaned_data['email']

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