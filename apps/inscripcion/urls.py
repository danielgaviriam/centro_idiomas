# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin

from views import *

urlpatterns = [
    url(r'^nuevo/',nueva_inscripcion, name='inscripcion_nuevo'),
    url(r'^solicitud_nuevo_idioma/',nuevo_idioma_inscripcion, name='inscripcion_nuevo_idioma'),
    url(r'^interfaz_continudad/',interfaz_continudad, name='interfaz_continudad'),
    
]

#Modulo de Administrador
"""
url(r'^listar_citas/',listar_citas, name='listar_citas'),
url(r'^confirmar_citas/',confirmacion_citas, name='confirmar_citas'),
url(r'^enviar_citas/',enviar_citas, name='enviar_citas'),
"""
#Ajax y Javascript
"""
url(r'^agregar_cita/',agregar_cita, name='agregar_cita'),
url(r'^cancelar_cita/',cancelar_cita, name='cancelar_cita'),
"""