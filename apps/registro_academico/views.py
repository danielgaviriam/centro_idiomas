# -*- coding: utf-8 -*-
# encoding: UTF-8
from django.shortcuts import render, redirect
from models import *
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
import traceback
from django.contrib import messages
from centro_idiomas.roles import *    
from rolepermissions.shortcuts import assign_role, get_user_role
from ..inscripcion.forms import ExamenForm


# Create your views here.
# Create your views here.
def nueva_citacion(request):
    #Validacion, para que el usuario que este registrado no pueda ingresar al formulario de inscripcion
    role = get_user_role(request.user)
    if request.user.is_anonymous() or role == Estudiante:
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        #recibir los datos
        form = CitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inscripcion:agendar_citas')
        else:
            form = CitacionForm()
            form.fields['responsable'].queryset = User.objects.filter(groups__name='calificador')
    else:
        form = CitacionForm()
        form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
    return render(request,'inscripcion/admin/citacion_form.html',{'form':form})

import json
def nueva_citacion_ajax(request):
    
    form = CitacionForm()
    
    return HttpResponse(form)
    
    
def editar_cita(request, id_cita):
    cita = Citacion.objects.get(id=id_cita)
    if request.method == 'GET':
        form = CitacionForm(instance=cita)
    else:
        form = CitacionForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
        return redirect('inscripcion:listar_citas')
        
    return render(request,'inscripcion/admin/citacion_form.html',{'form':form})

def eliminar_cita(request, id_cita):
    cita = Citacion.objects.get(id=id_cita)
    if request.method =='POST':
        cita.delete()
        return redirect('inscripcion:listar_citas')
    
    return render(request, 'inscripcion/admin/eliminar_citas.html', {'cita':cita})

#Auxiliar
from ..inscripcion.models import Inscripcion_Examen, Inscripcion

def cupos_disponbiles(id_citacion):
    examenes_asignados = 0
    examenes_totales = 0
    examenes_totales = Citacion.objects.get(pk=id_citacion)
    examenes_asignados = Inscripcion_Examen.objects.filter(citacion_id=id_citacion).count()
    
    return (examenes_totales.numero_estudiantes - examenes_asignados)

def cupos_asignados(id_citacion):
    examenes_asignados = Inscripcion_Examen.objects.filter(citacion_id=id_citacion).count()
    
    return (examenes_asignados)
    
def existen_citas(id_idioma, id_edad):
    cantidad_citaciones = Citacion.objects.filter(idioma=id_idioma,edad=id_edad).count()
    return cantidad_citaciones

from ..inscripcion.views import agendar_inscripcion
from ..inscripcion.models import Inscripcion

def agendar_citas(request):
    
    #Si usario no es anonimo? (ya esta log)
    role = get_user_role(request.user)
    if request.user.is_anonymous() or role == Estudiante:
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    
    contexto={   
    }
    if request.method == 'POST':
        tipo = str(request.POST.get('id_citacion_save'))
        idioma=request.POST.get('id_idioma_save')
        tap=idioma
        if tipo == "nuevo":
            form = CitacionForm(request.POST)
            if form.is_valid():
                idioma= Idioma.objects.get(nombre=idioma)
                citacion = form.save(commit=False)
                citacion.idioma=idioma
                citacion.save()
                ## agendamiento de citas
                inscripciones_pendientes = Inscripcion.objects.filter(cita_examen_creada=False,estado_inscripcion=True,idioma=idioma)
                for inscripcion in inscripciones_pendientes:
                    val = agendar_inscripcion(inscripcion)
            else:
                messages.error(request, "Esta intentando ingresar valores invalidos")
        else:
            cita = Citacion.objects.get(pk=tipo)
            cupos = cupos_asignados(tipo)
            form = CitacionForm(request.POST,instance=cita)
            if form.is_valid():
                idioma= Idioma.objects.get(nombre=idioma)
                citacion = form.save(commit=False)
                if (citacion.numero_estudiantes - cupos) < 0:
                    messages.error(request, "Esta intentando ingresar una cantidad de cupos inferior a los cuales ya hay asignados")
                else:
                    citacion.idioma=idioma
                    citacion.save()
                    inscripciones_pendientes = Inscripcion.objects.filter(cita_examen_creada=False,estado_inscripcion=True,idioma=idioma)
                    for inscripcion in inscripciones_pendientes:
                        val = agendar_inscripcion(inscripcion)
            else:
                messages.error(request, "Esta intentando ingresar valores invalidos")
    else:
        tap = request.GET.get('tap')
    
    if (tap == "Frances" ):
        #Set variables necesarias para este proceso
        idioma = Idioma.objects.get(nombre="Frances")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True,estado_inscripcion=False)
        preinscripciones_adultos =[] 
        preinscripciones_ninos = [] 
        for preinscripcion in preinscripciones:
            if preinscripcion.persona.mayor_de_edad == True:
                preinscripciones_adultos.append(preinscripcion)
            else:
                preinscripciones_ninos.append(preinscripcion)
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id).order_by('id')
        cantidad_citas_disponibles_adultos = 0
        cantidad_citas_disponibles_ninos = 0
        forms = []
        #Conformacion de Formularios para envio y posterior edicion en tabla del template
        for citacion in citaciones:
            if citacion.edad.id == 1:
                cantidad_citas_disponibles_adultos += cupos_disponbiles(citacion.id)
            else: 
                cantidad_citas_disponibles_ninos += cupos_disponbiles(citacion.id)
            form = CitacionForm(instance=citacion)
            form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
            obj = { 
                'id':citacion.id,
                'idioma':"Frances",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)
        
        empty_form=CitacionForm()
        empty_form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
        obj2={
            'idioma':"Frances",
            'form':empty_form,
            'nuevo':"nuevo"
        }
        forms.append(obj2)
        contexto['tap']="Frances"
        contexto['citaciones']=forms
        
        contexto['citaciones_no_disponibles_adultos']=preinscripciones_adultos
        contexto['citaciones_no_disponibles_ninos']=preinscripciones_ninos 
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)
        
    elif (tap == "Italiano" ):
        idioma = Idioma.objects.get(nombre="Italiano")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True)
        preinscripciones_adultos =[] 
        preinscripciones_ninos = [] 
        for preinscripcion in preinscripciones:
            if preinscripcion.persona.mayor_de_edad == True:
                preinscripciones_adultos.append(preinscripcion)
            else:
                preinscripciones_ninos.append(preinscripcion)
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id).order_by('id')
        cantidad_citas_disponibles_adultos = 0
        cantidad_citas_disponibles_ninos = 0
        forms = []
        #Conformacion de Formularios para envio y posterior edicion en tabla del template
        for citacion in citaciones:
            if citacion.edad.id == 1:
                cantidad_citas_disponibles_adultos += cupos_disponbiles(citacion.id)
            else: 
                cantidad_citas_disponibles_ninos += cupos_disponbiles(citacion.id)
            form = CitacionForm(instance=citacion)
            form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
            obj = { 
                'id':citacion.id,
                'idioma':"Italiano",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)
        
        empty_form=CitacionForm()
        empty_form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
        obj2={
            'idioma':"Italiano",
            'form':empty_form,
            'nuevo':"nuevo"
        }
        forms.append(obj2)
        contexto['tap']="Italiano"
        contexto['citaciones']=forms
        
        contexto['citaciones_no_disponibles_adultos']=preinscripciones_adultos
        contexto['citaciones_no_disponibles_ninos']=preinscripciones_ninos 
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)
        
    elif (tap == "Portugues" ):
        idioma = Idioma.objects.get(nombre="Portugues")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True)
        preinscripciones_adultos =[] 
        preinscripciones_ninos = [] 
        for preinscripcion in preinscripciones:
            if preinscripcion.persona.mayor_de_edad == True:
                preinscripciones_adultos.append(preinscripcion)
            else:
                preinscripciones_ninos.append(preinscripcion)
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id).order_by('id')
        cantidad_citas_disponibles_adultos = 0
        cantidad_citas_disponibles_ninos = 0
        forms = []
        #Conformacion de Formularios para envio y posterior edicion en tabla del template
        for citacion in citaciones:
            if citacion.edad.id == 1:
                cantidad_citas_disponibles_adultos += cupos_disponbiles(citacion.id)
            else: 
                cantidad_citas_disponibles_ninos += cupos_disponbiles(citacion.id)
            form = CitacionForm(instance=citacion)
            form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
            obj = { 
                'id':citacion.id,
                'idioma':"Portugues",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)    
        
        empty_form=CitacionForm()
        empty_form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
        obj2={
            'idioma':"Portugues",
            'form':empty_form,
            'nuevo':"nuevo"
        }
        forms.append(obj2)
        contexto['tap']="Portugues"
        contexto['citaciones']=forms
        
        contexto['citaciones_no_disponibles_adultos']=preinscripciones_adultos
        contexto['citaciones_no_disponibles_ninos']=preinscripciones_ninos 
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)
        
    else:
        idioma = Idioma.objects.get(nombre="Ingles")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True)
        preinscripciones_adultos =[] 
        preinscripciones_ninos = [] 
        for preinscripcion in preinscripciones:
            if preinscripcion.persona.mayor_de_edad == True:
                preinscripciones_adultos.append(preinscripcion)
            else:
                preinscripciones_ninos.append(preinscripcion)
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id).order_by('id')
        cantidad_citas_disponibles_adultos = 0
        cantidad_citas_disponibles_ninos = 0
        forms = []
        #Conformacion de Formularios para envio y posterior edicion en tabla del template
        for citacion in citaciones:
            if citacion.edad.id == 1:
                
                #cantidad_citas_disponibles_adultos += citacion.numero_estudiantes
                cantidad_citas_disponibles_adultos += cupos_disponbiles(citacion.id)
                
            else: 
                #cantidad_citas_disponibles_ninos += citacion.numero_estudiantes
                cantidad_citas_disponibles_ninos += cupos_disponbiles(citacion.id)
                
            form = CitacionForm(instance=citacion)
            form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
            obj = { 
                'id':citacion.id,
                'idioma':"Ingles",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)
        
        empty_form=CitacionForm()
        empty_form.fields["responsable"].queryset = User.objects.filter(groups__name='calificador')
        obj2={
            'idioma':"Ingles",
            'form':empty_form,
            'nuevo':"nuevo"
        }
        forms.append(obj2)
        contexto['tap']="Ingles"
        contexto['citaciones']=forms
        
        contexto['citaciones_no_disponibles_adultos']=preinscripciones_adultos
        contexto['citaciones_no_disponibles_ninos']=preinscripciones_ninos    
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)



from ..inscripcion.tables import CitacionTable
import json
from django.core import serializers
import datetime

def listar_citas(request):
    
    #Si usario no es anonimo? (ya esta log)
    role = get_user_role(request.user)
    if request.user.is_anonymous() or role == Estudiante:
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    
    contexto={
        
    }
    
    idioma1 = request.GET.get('tap')
    
    if idioma1 == None:
        idioma1="Ingles"
        
    idioma = Idioma.objects.get(nombre=idioma1)
    citaciones = Citacion.objects.filter(idioma_id=idioma.id)
    json_citaciones = serializers.serialize('json', citaciones)
    
    for citacion in citaciones:
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True,estado_inscripcion=True)
        citacion_mayor_edad = False
        
        if citacion.edad.descripcion_edad == "Adultos":
            citacion_mayor_edad = True
        else:
            citacion_mayor_edad = False
            
        control_loop =  cupos_disponbiles(citacion.id)  
        iterator = 0    
        for inscripcion in preinscripciones:
            if iterator == control_loop:
                break
            if inscripcion.persona.mayor_de_edad == citacion_mayor_edad:
                inscripcion.cita_examen_creada=True
                inscripcion.save()
                solicitud = Inscripcion_Examen(inscripcion=inscripcion, citacion = citacion, citacion_enviada=False)
                solicitud.save()
                iterator+=1
        
        
    lista =[]
    registros = Inscripcion_Examen.objects.filter(inscripcion__cita_examen_creada=True,inscripcion__idioma=idioma)
    for registro in registros:
        
        citaciones_disponibles = Citacion.objects.filter(idioma=registro.citacion.idioma,edad = registro.citacion.edad,fecha_examen__gte = datetime.date.today()).exclude(pk=registro.citacion.id)
        
        citas_disponibles = []
        for citas in citaciones_disponibles:
            cupos = cupos_disponbiles(citas.id)
            if cupos >0 :
                citas_disponibles.append(citas)
        
        form = ExamenForm(instance = registro)
        obj={
            'registro':registro,
            'form':form,
            'citas_disponibles':citas_disponibles,
        }
        lista.append(obj)
    
    contexto['current_date']=datetime.date.today()
    contexto['tap']=idioma1
    contexto['citaciones']=citaciones
    contexto['citas']=lista
    contexto['idioma']=idioma.nombre
    contexto['json_citaciones']=json_citaciones
    
    return render(request,'inscripcion/admin/listar_citas.html',contexto)

from django.core.mail import send_mail

def enviar_citas(request):
    
    idioma = request.GET.get('tap')
    idioma = Idioma.objects.get(nombre=idioma)
    
                
    registros = Inscripcion_Examen.objects.filter(inscripcion__cita_examen_creada=True,citacion_enviada=False,inscripcion__idioma=idioma)
    
    for registro in registros:
        mensaje = "Señor "+ str(registro.inscripcion.persona.nombres) + " " + str(registro.inscripcion.persona.apellidos) + " El Examen de Clasificacion para el Idioma " + str(registro.inscripcion.idioma.nombre) + ", quedo para  " + str(registro.citacion.fecha_examen) + ", en la sede " + str(registro.citacion.sede.nombre) + " en " + "ubicacion" + str(registro.citacion.salon) 
        send_mail(
            'Prueba Django',
            mensaje,
            'daga9420@gmail.com',
            [registro.inscripcion.persona.email],
            fail_silently=False,
            )
        registro.citacion_enviada = True
        registro.save()
    #Pendiente esta redirección    
    return redirect('inscripcion:agendar_citas')
    
    
def examen_disponible(id_idioma):
    examenes = Citacion.objects.filter(idioma=id_idioma)
    
    val = ""
    for examen in examenes:
        cupos = cupos_disponbiles(examen.id)
        if cupos > 0:
            val = examen
            return val
            
    return val