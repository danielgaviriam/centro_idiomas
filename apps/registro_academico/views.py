# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import *
from forms import *
from django.http import HttpResponseRedirect
from django.views.generic import ListView
import traceback

# Create your views here.
# Create your views here.
def nueva_citacion(request):
    #Validacion, para que el usuario que este registrado no pueda ingresar al formulario de inscripcion
    if request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        #recibir los datos
        form = CitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = CitacionForm()        
    else:
        form = CitacionForm()
    return render(request,'inscripcion/admin/citacion_form.html',{'form':form})
    
#Listar Basado en Clases
class Listar_citas(ListView):
    model = Citacion
    template_name = 'inscripcion/admin/listar_citas.html'
    
# Update Basdado en Clases


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

from ..inscripcion.views import Inscripcion

def agendar_citas(request):
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
            citacion = form.save(commit=False)
            citacion.idioma=idioma
            citacion.save()
            tap = idioma.nombre
    else:
        tap = request.GET.get('tap')
    
    if (tap == "Frances" ):
        #Set variables necesarias para este proceso
        idioma = Idioma.objects.get(nombre="Frances")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
        
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
                cantidad_citas_disponibles_adultos += citacion.numero_estudiantes
            else: 
                cantidad_citas_disponibles_ninos += citacion.numero_estudiantes
            form = CitacionForm(instance=citacion)
            obj = { 
                'id':citacion.id,
                'idioma':"Frances",
                'form':form,
                }
            forms.append(obj)
            
        contexto['tap']="Frances"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        for i in range(cantidad_citas_disponibles_adultos):
            try:
                posibles_citas_adultos.append(preinscripciones_adultos[i])
            except:
                print ""
        
        for preinscripcion in preinscripciones_adultos:
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        for i in range(cantidad_citas_disponibles_ninos):
            try:
                posibles_citas_ninos.append(preinscripciones_ninos[i])
            except:
                print ""
        
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
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
        
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
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
                cantidad_citas_disponibles_adultos += citacion.numero_estudiantes
            else: 
                cantidad_citas_disponibles_ninos += citacion.numero_estudiantes
            form = CitacionForm(instance=citacion)
            obj = { 
                'id':citacion.id,
                'idioma':"Italiano",
                'form':form,
                }
            forms.append(obj)
        
        
        contexto['tap']="Italiano"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        for i in range(cantidad_citas_disponibles_adultos):
            try:
                posibles_citas_adultos.append(preinscripciones_adultos[i])
            except:
                print ""
        
        for preinscripcion in preinscripciones_adultos:
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        for i in range(cantidad_citas_disponibles_ninos):
            try:
                posibles_citas_ninos.append(preinscripciones_ninos[i])
            except:
                print ""
        
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
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
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
                cantidad_citas_disponibles_adultos += citacion.numero_estudiantes
            else: 
                cantidad_citas_disponibles_ninos += citacion.numero_estudiantes
            form = CitacionForm(instance=citacion)
            obj = { 
                'id':citacion.id,
                'idioma':"Portugues",
                'form':form,
                }
            forms.append(obj)    
        
        contexto['tap']="Portugues"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        for i in range(cantidad_citas_disponibles_adultos):
            try:
                posibles_citas_adultos.append(preinscripciones_adultos[i])
            except:
                print ""
        
        for preinscripcion in preinscripciones_adultos:
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        for i in range(cantidad_citas_disponibles_ninos):
            try:
                posibles_citas_ninos.append(preinscripciones_ninos[i])
            except:
                print ""
        
        for preinscripcion in preinscripciones_ninos:
            if not preinscripcion in posibles_citas_ninos:
                citas_no_asignables_ninos.append(preinscripcion)
            
        
        contexto['citaciones_disponibles_adultos']=posibles_citas_adultos
        contexto['citaciones_no_disponibles_adultos']=citas_no_asignables_adultos
        contexto['citaciones_disponibles_ninos']=posibles_citas_ninos
        contexto['citaciones_no_disponibles_ninos']=citas_no_asignables_ninos
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)
        
    else:
        idioma = Idioma.objects.get(nombre="Ingles")
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
        
        preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
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
                cantidad_citas_disponibles_adultos += citacion.numero_estudiantes
            else: 
                cantidad_citas_disponibles_ninos += citacion.numero_estudiantes
                
            form = CitacionForm(instance=citacion)
            obj = { 
                'id':citacion.id,
                'idioma':"Ingles",
                'form':form,
                }
            forms.append(obj)
        
        contexto['tap']="Ingles"
        contexto['citaciones']=forms
        
        posibles_citas_adultos = []
        citas_no_asignables_adultos = []
        posibles_citas_ninos = []
        citas_no_asignables_ninos = []
        
        #Adultos
        for i in range(cantidad_citas_disponibles_adultos):
            try:
                posibles_citas_adultos.append(preinscripciones_adultos[i])
            except:
                print ""
        
        for preinscripcion in preinscripciones_adultos:
            if not preinscripcion in posibles_citas_adultos:
                citas_no_asignables_adultos.append(preinscripcion)
                
        #Ninos
        for i in range(cantidad_citas_disponibles_ninos):
            try:
                posibles_citas_ninos.append(preinscripciones_ninos[i])
            except:
                print ""
        
        for preinscripcion in preinscripciones_ninos:
            if not preinscripcion in posibles_citas_ninos:
                citas_no_asignables_ninos.append(preinscripcion)
            
        
        contexto['citaciones_disponibles_adultos']=posibles_citas_adultos
        contexto['citaciones_no_disponibles_adultos']=citas_no_asignables_adultos
        contexto['citaciones_disponibles_ninos']=posibles_citas_ninos
        contexto['citaciones_no_disponibles_ninos']=citas_no_asignables_ninos    
        
        return render(request,'inscripcion/admin/agendar_citas.html',contexto)
        
def enviar_citas(request):
    
    idioma = request.GET.get('tap')
    preinscripciones = Inscripcion.objects.filter(idioma_id=idioma.id,estado_inscripcion=False,sol_examen=True)
    preinscripciones_adultos =[] 
    preinscripciones_ninos = [] 
    for preinscripcion in preinscripciones:
        if preinscripcion.persona.mayor_de_edad == True:
            preinscripciones_adultos.append(preinscripcion)
        else:
            preinscripciones_ninos.append(preinscripcion)    
    citaciones = Citacion.objects.filter(idioma_id=idioma.id)