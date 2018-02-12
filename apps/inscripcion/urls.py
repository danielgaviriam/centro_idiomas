# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from ..registro_academico.views import nueva_citacion, listar_citas, editar_cita, eliminar_cita, agendar_citas,enviar_citas,nueva_citacion_ajax

from views import *

urlpatterns = [
    url(r'^nuevo/',nueva_inscripcion, name='inscripcion_nuevo'),
    url(r'^solicitud_nuevo_idioma/',nuevo_idioma_inscripcion, name='inscripcion_nuevo_idioma'),
    #url(r'^interfaz_continudad/',interfaz_continudad, name='interfaz_continudad'),
    #url(r'^agregar_continuidad/',formulario_de_continuacion, name='formulario_de_continuacion'),
    url(r'^gestion_inscripciones/',gestion_inscripciones, name='gestion_inscripciones'),
    url(r'^editar_inscripcion/(?P<id_inscripcion>\d+)/',editar_inscripcion, name='editar_inscripcion'),
    url(r'^eliminar_inscripcion/(?P<id_inscripcion>\d+)/',eliminar_inscripcion, name='eliminar_inscripcion'),
    url(r'^cargar_documentos/',carga_documentos, name='carga_documentos'),
    #Modulo de Citas (Administradores)
    url(r'^nueva_cita/',nueva_citacion, name='nueva_citacion'),
    url(r'^listar_citas/',listar_citas, name='listar_citas'),
    url(r'^editar_cita/(?P<id_cita>\d+)/$',editar_cita, name='editar_cita'),
    url(r'^eliminar/(?P<id_cita>\d+)/$',eliminar_cita, name='eliminar_cita'), 
    url(r'^agendar_citas/',agendar_citas, name='agendar_citas'),
    url(r'^enviar_citas/',enviar_citas, name='enviar_citas'),    
    
    #Financiera
    url(r'^matricula_financiera/',confirmar_matriculas, name='confirmar_matriculas'),    
    #Reportes
    url(r'^report/',reporte_examenes, name='reporte_examenes'),    
    #Ajax :)
    url(r'^cita_ajax/',nueva_citacion_ajax, name='nueva_citacion_ajax'),
    url(r'^guardar_notas/',guardar_notas_ajax, name='guardar_notas_ajax'),
    url(r'^get_frajas/',get_franjas, name='get_franjas'),
    
]