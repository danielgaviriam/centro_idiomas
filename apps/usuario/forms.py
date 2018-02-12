from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms




from django.contrib.auth.forms import AuthenticationForm

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-md','name':'username_login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-md'}))

from models import *

class RegistroForm(UserCreationForm):
    
    class Meta:
        model=User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
            #'Rol',
        ]
        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Email',
            'username':'Nombre de Usuario',
            'password1':'Contrasena',
            'password2':'Confirmacion de Contrasena',
        }
        widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-control'}),
			'last_name':forms.TextInput(attrs={'class':'form-control'}),
			'email':forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
			'username':forms.TextInput(attrs={'class':'form-control'}),
			'password1':forms.TextInput(attrs={'class':'form-control','type':'password'}),
			'password2':forms.TextInput(attrs={'class':'form-control','type':'password'}),
		}