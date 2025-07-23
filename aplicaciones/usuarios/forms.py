from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class UsuarioCreacionForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'apellidoP', 'apellidoM','email')  

class UsuarioCambioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'apellidoP', 'apellidoM','email')