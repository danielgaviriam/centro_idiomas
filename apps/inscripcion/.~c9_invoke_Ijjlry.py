# -*- coding: utf-8 -*-
from django import forms
from models import *

class PersonaForm(forms.ModelForm):
    
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
            'genero',
            'discapacidad',
            'nombre_acudiente',
            'telefono_acudiente',
            'email_acudiente',
            'numero_consignacion',
            ]
            #labels
        labels = {
            'tipo_identificacion':'Tipo de Identificación',
            'num_identificacion':'Numero de Identificacion',
            'nombres':'Nombres',
            'apellidos':'Apellidos',
            'ciudad':'Ciudad de Nacimiento',
            'tel_contacto':'Telefono de Contacto',
            'email':'Email',
            'edad':'Fecha de Nacimiento',
            'genero':'Sexo',
            'discapacidad':'Tiene alguna discapacidad',
            'nombre_acudiente': 'Nombre del Acudiente o contacto',
            'telefono_acudiente':'Celcular del Acudiente o contacto',
            'email_acudiente':'Email del Acudiente o contacto',
            'numero_consignacion':'Número de Consignación (Insc',
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
            'edad':forms.TextInput(attrs={'class':'form-control','type':'date'}), 
            'genero':forms.Select(attrs={'class':'form-control'}),
            'discapacidad':forms.Select(attrs={'class':'form-control'}),
            'nombre_acudiente':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_acudiente':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'email_acudiente':forms.TextInput(attrs={'class':'form-control','type':'email'}),
            'numero_consignacion':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            }
 

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
            #Campos especificados desde el modelo
        fields = [    
            'idioma',
            'sol_examen',
            'numero_consignacion',
            ]
            #labels
        labels = {
            'idioma':'Idioma',
            'sol_examen':'Examen de Clasificación',
            'numero_consignacion':'Número de Consignación',
            }
            #para poder dar clases a los campos
        widgets = {
            'idioma':forms.Select(attrs={'class':'form-control'}),
            'sol_examen':forms.RadioSelect(choices=[('1', 'True'), ('2', 'False')]),
            'numero_consignacion':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            }
            
class ExamenForm(forms.ModelForm):
    class Meta:
        model = Inscripcion_Examen
            #Campos especificados desde el modelo
        fields = [    
            'nota',
            'nivel_sugerido',
            ]
            #labels
        labels = {
            'nota':'nota',
            'nivel_sugerido':'nivel conseguido',
            }
        widgets = {
            'nota':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'nivel_sugerido':forms.Select(attrs={'class':'form-control'}),
            }

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documento
            #Campos especificados desde el modelo
        fields = [    
            'file_cedula',
            ]
            #labels
        labels = {
            'file_cedula':'Cargar Archivo',
            }