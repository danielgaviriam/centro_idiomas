# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..registro_academico.models import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from ..registro_academico.models import *

# Create your models here.

from django.core.validators import MinValueValidator
class Persona(models.Model):
    numero_consignacion = models.BigIntegerField(blank=False)
    tipo_identificacion = models.ForeignKey(Identificacion,blank=False)
    num_identificacion = models.BigIntegerField(blank=False)
    nombres = models.CharField(max_length=50,blank=False)
    apellidos = models.CharField(max_length=50,blank=False)
    ciudad = models.CharField(max_length=50,blank=False)
    tel_contacto = models.BigIntegerField(blank=False)
    email = models.EmailField(blank=False)
    edad = models.DateField(blank=False)
    mayor_de_edad = models.BooleanField(blank=True)
    discapacidad = models.ForeignKey(Discapacidad,null=True,blank=True)
    genero = models.ForeignKey(Genero,blank=False)
    #Datos Acudiente/Contacto 
    nombre_acudiente = models.CharField(max_length=50,blank=False)
    telefono_acudiente = models.BigIntegerField(blank=False)
    email_acudiente = models.EmailField(blank=False)
    usuario = models.ForeignKey(User,null=True,blank=True)
    
    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)
    
    def __unicode__(self):  
        return str(self.nombres)

#Modelo de Pre-Inscripcion
class Inscripcion(models.Model):
    persona = models.ForeignKey(Persona, blank=True)
    numero_consignacion = models.BigIntegerField(blank=True,null=True)
    idioma = models.ForeignKey(Idioma,blank=False)
    sol_examen = models.BooleanField(blank=True)
    estado_inscripcion = models.BooleanField(blank=True)
    cita_examen_creada = models.BooleanField(blank=True)
    franja = models.ForeignKey(Franja, blank=True)

    def __str__(self):
        return '{} {}'.format(self.idioma, self.persona.nombres)
    
    def __unicode__(self):  
        return str(self.persona.nombres)

        
class Solicitud_Continuacione(models.Model):
    persona = models.ForeignKey(Persona,null=True,blank=False)
    pre_curso = models.ForeignKey(Curso,null=True,blank=False)
    idioma = models.ForeignKey(Idioma,null=True,blank=False)
    nivel = models.ForeignKey(Nivel,null=True,blank=False)
    confirmacion = models.BooleanField()

    def __str__(self):
        return '{} {} {}'.format(self.persona.nombres, self.pre_curso.nombre, self.pre_curso.nivel)

class Inscripcion_Examen(models.Model):
    nota = models.FloatField(null=True, blank=True)
    inscripcion = models.ForeignKey(Inscripcion)
    citacion = models.ForeignKey(Citacion,)
    citacion_enviada = models.BooleanField()
    nivel_sugerido = models.ForeignKey(Nivel,blank=True,null=True)
    
    def __str__(self):
        return '{}'.format(self.inscripcion.persona.nombres)
        
class Documento(models.Model):
    persona = models.ForeignKey(Persona,blank=False)
    file_cedula = models.FileField(upload_to='imagenes/di/')
    
    def __str__(self):
        return '{}'.format(self.persona.nombres)