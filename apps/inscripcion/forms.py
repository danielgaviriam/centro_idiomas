# -*- coding: utf-8 -*-
from django import forms
from models import *

class PersonaForm(forms.ModelForm):
    
    nombre_acudiente = forms.CharField(required=False)
    ocupacion_acudiente = forms.CharField(required=False)
    telefono_acudiente = forms.CharField(required=False)
    email_acudiente = forms.CharField(required=False)
    
    class Meta:
        model = Persona
            #Campos especificados desde el modelo
        fields = [
            'tipo_identificacion',
            'num_identificacion',
            'nombres',
            'apellidos',
            'ciudad',
            'tel_contacto',
            'email',
            'edad',
            'discapacidad',
            'nombre_acudiente',
            'ocupacion_acudiente',
            'telefono_acudiente',
            'email_acudiente',
            ]
            #labels
        labels = {
            'tipo_identificacion':'Tipo de Identificación',
            'num_identificacion':'Numero de Identificacion',
            'nombres':'Nombres Completos',
            'apellidos':'Apellidos',
            'ciudad':'Ciudad de Nacimiento',
            'tel_contacto':'Telefono de Contacto',
            'email':'Email',
            'edad':'Edad',
            'discapacidad':'Tiene alguna discapacidad',
            'nombre_acudiente': 'Nombre del Acudiente',
            'ocupacion_acudiente':'Ocupacion del Acudiente',
            'telefono_acudiente':'Celcular del Acudiente',
            'email_acudiente':'Email del Acudiente',
            }
            #para poder dar clases a los campos
        widgets = {
            'tipo_identificacion':forms.Select(attrs={'class':'form-control'}),
            'num_identificacion':forms.TextInput(attrs={'class':'form-control','type':'number'}),    
            'nombres':forms.TextInput(attrs={'class':'form-control'}),
            'apellidos':forms.TextInput(attrs={'class':'form-control'}),
            'ciudad':forms.TextInput(attrs={'class':'form-control'}),
            'tel_contacto':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'email':forms.TextInput(attrs={'class':'form-control','type':'email'}),
            'edad':forms.TextInput(attrs={'class':'form-control','type':'number'}),    
            'discapacidad':forms.Select(attrs={'class':'form-control'}),
            'nombre_acudiente':forms.TextInput(attrs={'class':'form-control','required': False}),
            'ocupacion_acudiente':forms.TextInput(attrs={'class':'form-control','required': False}),
            'telefono_acudiente':forms.TextInput(attrs={'class':'form-control','type':'number','required': False}),
            'email_acudiente':forms.TextInput(attrs={'class':'form-control','type':'email','required': False}),
            }
 

class InscripcionForm(forms.ModelForm):
    
    class Meta:
        model = Inscripcion
            #Campos especificados desde el modelo
        fields = [    
            'ciclo_academico',
            'idioma',
            'sol_examen',
            ]
            #labels
        labels = {
            'ciclo_academico':'Ciclo academico al cual desea ingresar',
            'idioma':'Idioma',
            'sol_examen':'Examen de Clasificación',
            }
            #para poder dar clases a los campos
        widgets = {
            'ciclo_academico':forms.Select(attrs={'class':'form-control'}),
            'idioma':forms.Select(attrs={'class':'form-control'}),
            'sol_examen':forms.RadioSelect(choices=[('1', 'True'), ('2', 'False')]),
            }