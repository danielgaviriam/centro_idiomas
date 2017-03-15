# -*- coding: utf-8 -*-
from django import forms
from models import *

class CursoForm(forms.ModelForm):
    
    #Class meta permite identificar el 
    #modelo del cual se le va a crear el form
    
    class Meta:
        model = Curso
            #Campos especificados desde el modelo
        fields = [
            'ciclo',
            'sede',
            'idioma',
            'nivel',
            'jornada',
            'edad',
            ]
            #labels
        labels = {
            'ciclo':'Ciclo Curso',
            'sede':'Sede Curso',
            'idioma':'Idioma Curso',
            'nivel':'Nivel Curso',
            'jornada':'Jornada Curso',
            'edad':'Edades Curso',
            }
            #para poder dar clases a los campos
        widgets = {
            'ciclo':forms.Select(attrs={'class':'form-control'}),
            'idioma':forms.Select(attrs={'class':'form-control'}),
            'sede':forms.Select(attrs={'class':'form-control'}),
            'nivel':forms.Select(attrs={'class':'form-control'}),
            'jornada':forms.Select(attrs={'class':'form-control'}),
            'edad':forms.Select(attrs={'class':'form-control'}),
            }
            
class CitacionForm(forms.ModelForm):
    
    #Class meta permite identificar el 
    #modelo del cual se le va a crear el form
    
    class Meta:
        model = Citacion
            #Campos especificados desde el modelo
        fields = [
            'fecha_examen',
            'sede',
            'idioma',
            'edad',
            'salon',
            'numero_estudiantes',
            ]
            #labels
        labels = {
            'fecha_examen':'Fecha de Examen',
            'sede':'Sede de examen',
            'idioma':'Idioma de Examen',
            'edad':'Tipo de Examen',
            'salon':'Ubicacion',
            'numero_estudiantes':'Capacidad Examen',
            }
            #para poder dar clases a los campos
        widgets = {
            'fecha_examen':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            'sede':forms.Select(attrs={'class':'form-control'}),
            'idioma':forms.Select(attrs={'class':'form-control'}),
            'edad':forms.Select(attrs={'class':'form-control'}),
            'salon':forms.TextInput(attrs={'class':'form-control'}),
            }
            