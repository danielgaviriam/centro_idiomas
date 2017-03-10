# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^registro_usuario/',registro_usuarios, name='registro_usuarios'),
    url(r'^cerrar_sesion/',cerrar_sesion, name='cerrar_sesion'),
]