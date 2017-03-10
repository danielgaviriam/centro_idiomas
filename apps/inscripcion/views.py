# -*- coding: utf-8 -*-
#!/usr/local/bin/python
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from forms import *
from models import *
from ..registro_academico.models import Citacion, Idioma, Sede, Matricula, Nivel
from centro_idiomas.roles import *    
from rolepermissions.shortcuts import assign_role, get_user_role



# Create your views here.
def nueva_inscripcion(request):
    #Validacion, para que el usuario que este registrado no pueda ingresar al formulario de inscripcion
    if not request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        #recibir los datos
        form = PersonaForm(request.POST)
        form2 = InscripcionForm(request.POST)
        if (form.is_valid() and form2.is_valid()):
            data_persona = form.cleaned_data
            data_inscripcion = form2.cleaned_data
            
            
            existe = Persona.objects.filter(num_identificacion = data_persona['num_identificacion']).count()
            
            if(existe != 0):
                messages.error(request, "Su Identificacion ya se encuentra registrada")
                form = PersonaForm()
                form2 = InscripcionForm()
            else:
                edad_inscripcion = int(data_persona['edad'])
                persona = form.save(commit=False)
                inscripcion = form2.save(commit=False)
                if(edad_inscripcion < 17):
                    persona.mayor_de_edad = False
                else:
                    persona.mayor_de_edad = True
                    
                persona.telefono_acudiente = 0
                    
                inscripcion.estado_inscripcion=False
                inscripcion.cita_examen_creada=False
                user = User.objects.create_user(username=persona.num_identificacion,
                                 email=persona.email,
                                 password=persona.num_identificacion)
                persona.usuario = user
                
                assign_role(user,'estudiante')
                form.save()
                persona_almacenada = Persona.objects.get(num_identificacion=persona.num_identificacion)
                inscripcion.persona = persona_almacenada
                inscripcion.save()    
                
                return redirect('index')
    else:
        form = PersonaForm()
        form2 = InscripcionForm()
    
    return render(request,'inscripcion/user/inscripcion_form.html',{'form':form, 'form2':form2})
    
def nuevo_idioma_inscripcion(request):
    
    if request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        #recibir los datos
        form2 = InscripcionForm(request.POST)
        if form2.is_valid():
            usuario_actual=request.user
            persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
            
            
            data_inscripcion = form2.cleaned_data
            existe = Inscripcion.objects.filter(persona_id=persona_logged.id,idioma_id = data_inscripcion['idioma'],ciclo_academico_id=data_inscripcion['ciclo_academico']).count()
            if(existe != 0):
                messages.error(request, "Usted ya ha realizado esta inscripcion")
                form = InscripcionForm()
            else:    
                inscripcion = form2.save(commit=False)
                inscripcion.estado_inscripcion=False
                inscripcion.cita_examen_creada=False
                inscripcion.persona = persona_logged
                inscripcion.save()    
                return redirect('index')
    else:
        form = InscripcionForm()
    
    return render(request,'inscripcion/user/solicitud_nuevo_idioma.html',{'form':form})

def interfaz_continudad(request):
    
    #Usuario/Persona logged
    usuario_actual=request.user
    persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
    #Idiomas en los que se encuentra matriculado
    lista_idiomas=[]
    lista_estudiante_niveles_notas=[]
    
    matriculas = Matricula.objects.filter(persona_id=persona_logged.id)
    for matricula in matriculas:    
        lista_idiomas.append(matricula.curso.idioma.id)
        
        obj = {
            'idioma':matricula.curso.idioma,
            'nivel':matricula.curso.nivel,
            'nota':matricula.nota,
        }
        lista_estudiante_niveles_notas.append(obj)
        
    idiomas = Idioma.objects.filter(pk__in=lista_idiomas)
    
    niveles = Nivel.objects.all()
    contexto = {'idiomas':idiomas,'niveles':niveles,'lista_estudiante':lista_estudiante_niveles_notas}
    
    return render(request,'inscripcion/user/interfaz_continuidad.html',contexto)
    
    
"""
def listar_citas(request):
    
    #Validacion de Rol
    usuario_log = request.user
    role = get_user_role(usuario_log)
    if role == Estudiante:
        return HttpResponseRedirect('/index')
    #queryset
    inscripcion = pre_inscripcion.objects.all().order_by('id')
    citacion = Citacion.objects.all().order_by('id')
    solicitudes_atendidas = preinscripcion_examen.objects.all().order_by('id')
    contexto = {'pre_inscripcion':inscripcion,'citacion':citacion,'solicitudes_atendidas':solicitudes_atendidas}
    return render(request, 'inscripcion/admin/listar_citas.html',contexto)
    
def agregar_cita(request):
    pre_inscrito = request.GET.get('identificador_inscripcion')
    cita_asignada = request.GET.get('identificador_citacion')
    #COnsultas a la Base de datos
    registro_preinscripcion = pre_inscripcion.objects.get(pk = pre_inscrito)
    registro_preinscripcion.cita_creada=True
    registro_citacion = Citacion.objects.get(pk = cita_asignada)
    #Creacion de registro
    agenda_cita = preinscripcion_examen()
    agenda_cita.usuario_preinscrito = registro_preinscripcion
    agenda_cita.citacion = registro_citacion
    agenda_cita.nota = None
    agenda_cita.citacion_enviada = False
    registro_preinscripcion.save()
    #Almacenamiento de registro
    agenda_cita.save()
    
    return HttpResponse(True)

def cancelar_cita(request):
    pre_inscrito = request.GET.get('identificador_inscripcion')
    cita_asignada = request.GET.get('identificador_citacion')
    #COnsultas a la Base de datos
    registro_preinscripcion = pre_inscripcion.objects.get(pk = pre_inscrito)
    registro_citacion = Citacion.objects.get(pk = cita_asignada)
    #Creacion de registro
    citacion_eliminar = preinscripcion_examen.objects.filter(usuario_preinscrito=registro_preinscripcion, citacion=registro_citacion)
    citacion_eliminar.delete()
    registro_preinscripcion.cita_creada=False
    registro_preinscripcion.save()
    return HttpResponse(citacion_eliminar)
    

def confirmacion_citas(request):
     #Validacion de Rol
    usuario_log = request.user
    role = get_user_role(usuario_log)
    if role == Estudiante:
        return HttpResponseRedirect('/index')
    inscripciones_confirmadas = list(pre_inscripcion.objects.filter(cita_creada = True))
    citaciones = Citacion.objects.all().order_by('id')
    contexto = {'pre_inscripcion':inscripciones_confirmadas,'citacion':citaciones}
    return render(request, 'inscripcion/admin/confirmar_citas.html',contexto)
    

from django.core.mail import send_mail
import psycopg2, psycopg2.extras
import traceback



def enviar_citas(request):
    inscripciones_confirmadas = pre_inscripcion.objects.filter(cita_creada = True)
    try:
        connection = psycopg2.connect(database='centro_idiomas_bd',user='postgres',password='postgres', host='localhost')
        cursor = connection.cursor()
        cursor.execute("select * from registro_academico_citacion JOIN (select * from (select id, email, nombres, apellidos from inscripcion_pre_inscripcion where cita_creada = True) as inscritos JOIN inscripcion_preinscripcion_examen ON inscritos.id = inscripcion_preinscripcion_examen.usuario_preinscrito_id) as usuarios ON registro_academico_citacion.id = usuarios.citacion_id")
        datos_email = cursor.fetchall()
        
        for datos in datos_email:
            idioma = Idioma.objects.get(pk=datos[5])
            
            sede = Sede.objects.get(pk=datos[6])
            
            registro = preinscripcion_examen.objects.get(pk=datos[11])
            registro.citacion_enviada = True
            registro.save()
            
            mensaje = "Señor "+ str(datos[9]) + " " + str(datos[10]) + " El Examen de Clasificacion para el Idioma " + str(idioma.nombre) + ", quedo para  " + str(datos[1]) + ", en la sede " + str(sede.nombre) + " en " + "ubicacion" + str(datos[2])
            send_mail(
                'Prueba Django',
                mensaje,
                'daga9420@gmail.com',
                [datos[8]],
                fail_silently=False,
                )
    except:
        print "fallo"
        traceback.print_exc()

    return render(request, 'index.html')
    
        
"""