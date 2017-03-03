from __future__ import unicode_literals

from django.db import models

from ..registro_academico.models import Identificacion, Edad, Discapacidad

# Create your models here.

#Modelo de Pre-Inscripcion
class pre_inscripcion(models.Model):
    tipo_identificacion = models.ForeignKey(Identificacion,null=True,blank=True)
    num_identificacion = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    tel_contacto = models.IntegerField()
    email = models.EmailField()
    sol_examen = models.BooleanField()
    edad = models.IntegerField()
    edad_clasificacion = models.ForeignKey(Edad,null=True,blank=True)
    discapacidad = models.ForeignKey(Discapacidad,null=True,blank=True)
    estado_inscripcion = models.BooleanField()
    