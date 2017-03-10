# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..registro_academico.models import Identificacion, Discapacidad, Idioma, Ciclo #,Citacion
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class Persona(models.Model):
    tipo_identificacion = models.ForeignKey(Identificacion,null=True,blank=True)
    num_identificacion = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    tel_contacto = models.BigIntegerField()
    email = models.EmailField()
    edad = models.IntegerField()
    mayor_de_edad = models.BooleanField(blank=True)
    discapacidad = models.ForeignKey(Discapacidad,null=True,blank=True)
    #Datos Acudiente
    nombre_acudiente = models.CharField(max_length=50, null=True)
    ocupacion_acudiente = models.CharField(max_length=50, null=True)
    telefono_acudiente = models.BigIntegerField(null = True, blank=True)
    email_acudiente = models.EmailField(null=True)
    usuario = models.ForeignKey(User,null=True,blank=True)
    
    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

#Modelo de Pre-Inscripcion
class Inscripcion(models.Model):
    persona = models.ForeignKey(Persona,null=True,blank=True)
    idioma = models.ForeignKey(Idioma,null=True,blank=True)
    sol_examen = models.BooleanField()
    estado_inscripcion = models.BooleanField()
    cita_examen_creada = models.BooleanField()
    ciclo_academico = models.ForeignKey(Ciclo,null=True,blank=True)

    def __str__(self):
        return '{} {}'.format(self.idioma, self.persona.nombres)
        
"""
class preinscripcion_examen(models.Model):
    nota = models.IntegerField(null=True)
    usuario_preinscrito = models.ForeignKey(pre_inscripcion,null=True,blank=True)
    citacion = models.ForeignKey(Citacion,null=True,blank=True)
    citacion_enviada = models.BooleanField()
    
    def __str__(self):
        return '{}'.format(self.usuario_preinscrito.num_identificacion)
    
    def __unicode__(self):
        return self.nota or u''"""