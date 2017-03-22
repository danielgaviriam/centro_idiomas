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
import psycopg2, psycopg2.extras
import traceback

# Create your views here.
def nueva_inscripcion(request):
    #Validacion, para que el usuario que este registrado no pueda ingresar al formulario de inscripcion
    role = get_user_role(request.user)
    if role == Estudiante:
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
    if request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    #Usuario/Persona logged
    usuario_actual=request.user
    persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
    
    
    try:
        connection = psycopg2.connect(database='centro_idiomas_bd',user='postgres',password='postgres', host='localhost')
        cursor = connection.cursor()
        cursor.execute("select mat.persona_id, c.idioma_id,c.nivel_id, MAX(mat.nota) from (select id, idioma_id,nivel_id from registro_academico_curso) as c JOIN registro_academico_matricula as mat ON c.id = mat.curso_id where persona_id= " + str(persona_logged.id) + "group by persona_id, idioma_id, nivel_id;")
        datos_curso = cursor.fetchall()
        
        niveles = Nivel.objects.all().values_list('id',flat=True)
        lista_idiomas = []
        
        for datos in datos_curso:
            if not datos[1] in lista_idiomas:
                lista_idiomas.append(datos[1])
        #Buscar como hacerlo mas facil!! NOTAAA!!                
        idiomas_vistos = Idioma.objects.filter(pk__in=lista_idiomas)
        informacion = []
        for idioma in idiomas_vistos:
            niveles_vistos=[]
            nivel_nota = []
            for nivel in niveles:
                for dato in datos_curso:
                    if dato[2] == nivel and dato[1] == idioma.id and dato[3] >= 3:
                        niveles_vistos.append(dato[2])
                        nivel_a_asignar = Nivel.objects.get(pk=dato[2])
                        obj={
                            'nivel':nivel_a_asignar.nombre,
                            'nota':dato[3],
                            'disponible':False
                        }
                        nivel_nota.append(obj)
            
            for nivel in niveles:
                if not nivel in niveles_vistos:
                    nivel_a_asignar = Nivel.objects.get(pk=nivel)
                    if nivel_a_asignar.pre_requisito_id in niveles_vistos:
                        obj={
                                'nivel':nivel_a_asignar.nombre,
                                'nota':-1,
                                'disponible':True
                            }
                        nivel_nota.append(obj)
                    else:
                        obj={
                                'nivel':nivel_a_asignar.nombre,
                                'nota':-1,
                                'disponible':False
                            }
                        nivel_nota.append(obj)
            
            obj2={
                'idioma':idioma.nombre,
                'niveles':nivel_nota,
            }
            informacion.append(obj2)
            
            
        return render(request,'inscripcion/user/interfaz_continuidad.html',{'informacion':informacion})
    except:
        print "fallo"
        traceback.print_exc()
        return render(request,'inscripcion/user/interfaz_continuidad.html')
    

def formulario_de_continuacion(request):
    
    #Usuario/Persona logged
    if request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    usuario_actual=request.user
    persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
    
    #Variables de AJAX
    variable_a = request.GET.get('identificador_idioma')
    id_idioma = Idioma.objects.get(nombre=variable_a)
    variable_b = request.GET.get('identificador_nivel')
    id_nivel = Nivel.objects.get(nombre=variable_b)
    try:
        existe = Solicitud_Continuacione.objects.filter(idioma=id_idioma,nivel=id_nivel).count()
        if existe != 0:
            return HttpResponse(-1)
            
        connection = psycopg2.connect(database='centro_idiomas_bd',user='postgres',password='postgres', host='localhost')
        cursor = connection.cursor()
        cursor.execute("select c.id, MAX(mat.nota) from (select curso_id, nota from registro_academico_matricula where persona_id = " + str(persona_logged.id) + ") as mat JOIN registro_academico_curso as c ON c.id = mat.curso_id where idioma_id=" + str(id_idioma.id) + " AND nivel_id= "+ str(id_nivel.pre_requisito_id) +" GROUP BY c.id;")
        datos_curso = cursor.fetchall()
        
        for datos in datos_curso:
            id_curso = datos[0]
            nota = datos[1]
        
        curso = Curso.objects.get(pk=id_curso)
        if nota >= 3:
            
            solicitud = Solicitud_Continuacione(persona_id=persona_logged.id,pre_curso_id=curso.id,confirmacion=False,idioma=id_idioma,nivel=id_nivel)
            solicitud.save()
            return HttpResponse(1)    
        else:
            return HttpResponse(0)
        
    except:
        traceback.print_exc()
        return HttpResponse(0)
        

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
        
        traceback.print_exc()

    return render(request, 'index.html')
    
        
"""