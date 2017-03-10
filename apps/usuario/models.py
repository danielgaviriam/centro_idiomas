from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Usuario_permisos(models.Model):
    nombre_usuario = models.CharField(max_length=50)
    
    def __str__(self):
        return '{}'.format(self.nombre_usuario)