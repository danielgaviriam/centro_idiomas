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