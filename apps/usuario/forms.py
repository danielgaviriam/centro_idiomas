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
            #'Rol',
        ]
        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Email',
            'username':'Nombre de Usuario',
            #'Rol':'Rol de Sistema',
        }
        widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-control'}),
			'last_name':forms.TextInput(attrs={'class':'form-control'}),
			'email':forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
			'username':forms.TextInput(attrs={'class':'form-control'}),
			#'Rol':forms.Select(attrs={'class':'form-control'}),
		}