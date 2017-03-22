# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import *
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
import traceback
from django.contrib import messages
from centro_idiomas.roles import *    
from rolepermissions.shortcuts import assign_role, get_user_role

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
    else:
        form = CitacionForm()
    return render(request,'inscripcion/admin/citacion_form.html',{'form':form})

import json
def nueva_citacion_ajax(request):
    
    form = CitacionForm()
    
    return HttpResponse(form)
    
    
#Listar Basado en Clases
class Listar_citas(ListView):
    model = Citacion
    template_name = 'inscripcion/admin/listar_citas.html'
    

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
    
def existen_citas(id_idioma, id_edad):
    cantidad_citaciones = Citacion.objects.filter(idioma=id_idioma,edad=id_edad).count()
    return cantidad_citaciones

from ..inscripcion.views import Inscripcion

def agendar_citas(request):
    
    #Si usario no es anonimo? (ya esta log)
    role = get_user_role(request.user)
    if request.user.is_anonymous() or role == Estudiante:
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    
    contexto={   
    }
    if request.method == 'POST':
        id_cita = request.POST.values()
        if id_cita[6] == "Ingles":
            idioma = Idioma.objects.get(nombre="Ingles")
        else:
            idioma = Idioma.objects.get(nombre=str(id_cita[4]))
        cita = Citacion.objects.get(pk=id_cita[2])
        form = CitacionForm(request.POST,instance=cita)
        tap = str(idioma.nombre)
        if form.is_valid():
            try:
                citacion = form.save(commit=False)
                citacion.idioma=idioma
                citacion.save()
                tap = idioma.nombre
            except:
                messages.error(request, "Esta intentando ingresar valores invalidos")
                tap = request.GET.get('tap')    
        else:
            messages.error(request, "Esta intentando ingresar valores invalidos")
            tap = request.GET.get('tap')
    else:
        tap = request.GET.get('tap')
    
    if (tap == "Frances" ):
        #Set variables necesarias para este proceso
        idioma = Idioma.objects.get(nombre="Frances")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True)
        preinscripciones_adultos =[] 
        preinscripciones_ninos = [] 
        for preinscripcion in preinscripciones:
            if preinscripcion.persona.mayor_de_edad == True:
                preinscripciones_adultos.append(preinscripcion)
            else:
                preinscripciones_ninos.append(preinscripcion)
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id)
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
            obj = { 
                'id':citacion.id,
                'idioma':"Frances",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)
            
        contexto['tap']="Frances"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        control_loop =  cantidad_citas_disponibles_adultos
        iterator = 0    
        
        for preinscripcion in preinscripciones_adultos:
            if iterator == control_loop:
                break
            posibles_citas_adultos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_adultos:
            
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        control_loop =  cantidad_citas_disponibles_ninos
        iterator = 0    
        
        for preinscripcion in preinscripciones_ninos:
            if iterator == control_loop:
                break
            posibles_citas_ninos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_ninos:
            
            if not preinscripcion in posibles_citas_ninos:
                citas_no_asignables_ninos.append(preinscripcion)
            
        
        contexto['citaciones_disponibles_adultos']=posibles_citas_adultos
        contexto['citaciones_no_disponibles_adultos']=citas_no_asignables_adultos
        contexto['citaciones_disponibles_ninos']=posibles_citas_ninos
        contexto['citaciones_no_disponibles_ninos']=citas_no_asignables_ninos
        
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
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id)
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
            obj = { 
                'id':citacion.id,
                'idioma':"Italiano",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)
        
        
        contexto['tap']="Italiano"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        control_loop =  cantidad_citas_disponibles_adultos
        iterator = 0    
        
        for preinscripcion in preinscripciones_adultos:
            if iterator == control_loop:
                break
            posibles_citas_adultos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_adultos:
            
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        control_loop =  cantidad_citas_disponibles_ninos
        iterator = 0    
        
        for preinscripcion in preinscripciones_ninos:
            if iterator == control_loop:
                break
            posibles_citas_ninos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_ninos:
            
            if not preinscripcion in posibles_citas_ninos:
                citas_no_asignables_ninos.append(preinscripcion)
            
        
        contexto['citaciones_disponibles_adultos']=posibles_citas_adultos
        contexto['citaciones_no_disponibles_adultos']=citas_no_asignables_adultos
        contexto['citaciones_disponibles_ninos']=posibles_citas_ninos
        contexto['citaciones_no_disponibles_ninos']=citas_no_asignables_ninos
        
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
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id)
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
            obj = { 
                'id':citacion.id,
                'idioma':"Portugues",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)    
        
        contexto['tap']="Portugues"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        control_loop =  cantidad_citas_disponibles_adultos
        iterator = 0    
        
        for preinscripcion in preinscripciones_adultos:
            if iterator == control_loop:
                break
            posibles_citas_adultos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_adultos:
            if (existen_citas(idioma.id,1) == 0):
                citas_no_asignables_adultos.append(preinscripcion)
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        control_loop =  cantidad_citas_disponibles_ninos
        iterator = 0    
        
        for preinscripcion in preinscripciones_ninos:
            if iterator == control_loop:
                break
            posibles_citas_ninos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_ninos:
            if (existen_citas(idioma.id,2) == 0):
                citas_no_asignables_ninos.append(preinscripcion)
                
            if not preinscripcion in posibles_citas_ninos:
                citas_no_asignables_ninos.append(preinscripcion)
            
        contexto['citaciones_disponibles_adultos']=posibles_citas_adultos
        contexto['citaciones_no_disponibles_adultos']=citas_no_asignables_adultos
        contexto['citaciones_disponibles_ninos']=posibles_citas_ninos
        contexto['citaciones_no_disponibles_ninos']=citas_no_asignables_ninos
        
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
        
        citaciones = Citacion.objects.filter(idioma_id=idioma.id)
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
            obj = { 
                'id':citacion.id,
                'idioma':"Ingles",
                'form':form,
                'cupos':cupos_disponbiles(citacion.id)
                }
            forms.append(obj)
        
        contexto['tap']="Ingles"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        control_loop =  cantidad_citas_disponibles_adultos
        iterator = 0    
        
        for preinscripcion in preinscripciones_adultos:
            if iterator == control_loop:
                break
            posibles_citas_adultos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_adultos:    
            
            if (existen_citas(idioma.id,1) == 0):
                citas_no_asignables_adultos.append(preinscripcion)
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        control_loop =  cantidad_citas_disponibles_ninos
        iterator = 0    
        
        for preinscripcion in preinscripciones_ninos:
            if iterator == control_loop:
                break
            posibles_citas_ninos.append(preinscripcion)
            iterator += 1
        
        for preinscripcion in preinscripciones_ninos:
            
            if (existen_citas(idioma.id,2) == 0):
                citas_no_asignables_ninos.append(preinscripcion)
                
            if not preinscripcion in posibles_citas_ninos:
                citas_no_asignables_ninos.append(preinscripcion)
            
        
        contexto['citaciones_disponibles_adultos']=posibles_citas_adultos
        contexto['citaciones_no_disponibles_adultos']=citas_no_asignables_adultos
        contexto['citaciones_disponibles_ninos']=posibles_citas_ninos
        contexto['citaciones_no_disponibles_ninos']=citas_no_asignables_ninos    
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)


from django.core.mail import send_mail

def enviar_citas(request):
    
    idioma = request.GET.get('tap')
    idioma = Idioma.objects.get(nombre=idioma)
    citaciones = Citacion.objects.filter(idioma_id=idioma.id)
    
    for citacion in citaciones:
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,cita_examen_creada=False,sol_examen=True)
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
                solicitud = Inscripcion_Examen(inscripcion=inscripcion, citacion = citacion, citacion_enviada=False, nota=-1)
                solicitud.save()
                iterator+=1
                
    registros = Inscripcion_Examen.objects.filter(inscripcion__cita_examen_creada=True,citacion_enviada=False)
    
    for registro in registros:
        mensaje = "Señor "+ str(registro.inscripcion.persona.nombres) + " " + str(registro.inscripcion.persona.apellidos) + " El Examen de Clasificacion para el Idioma " + str(registro.inscripcion.idioma.nombre) + ", quedo para  " + str(registro.citacion.fecha_examen) + ", en la sede " + str(registro.citacion.sede.nombre) + " en " + "ubicacion" + str(registro.citacion.salon)
        send_mail(
            'Prueba Django',
            mensaje,
            'daga9420@gmail.com',
            [registro.inscripcion.persona.email],
            fail_silently=False,
            )
        
    return HttpResponseRedirect('/inscripcion/agendar_citas/?tap='+idioma.nombre)
    
    

            
    


    
    