# -*- coding: utf-8 -*-
#!/usr/local/bin/python
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from forms import *
from models import *
from ..registro_academico.models import Citacion, Idioma, Sede, Matricula, Nivel
from ..registro_academico.views import cupos_disponbiles
from centro_idiomas.roles import *    
from rolepermissions.shortcuts import assign_role, get_user_role
import psycopg2, psycopg2.extras
import traceback
import datetime 

# Create your views here.

def agendar_inscripcion(inscripcion):
    if inscripcion.persona.mayor_de_edad == True:
        citaciones_disponibles = Citacion.objects.filter(idioma=inscripcion.idioma,edad=1)
    else:
        citaciones_disponibles = Citacion.objects.filter(idioma=inscripcion.idioma,edad=2)
        
    check = False
    for citas in citaciones_disponibles:
        if cupos_disponbiles(citas.id)>0:
            solicitud = Inscripcion_Examen(inscripcion=inscripcion, citacion = citas, citacion_enviada=False)
            solicitud.save()
            check = True
            break
    
    if check == True:
        inscripcion.cita_examen_creada=True
        inscripcion.save()
        return True
    else:
        return False
            

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
            try:
                franja = request.POST.get('franja')
                data_persona = form.cleaned_data
                data_inscripcion = form2.cleaned_data
                edad_inscripcion = data_persona['edad']
                diferencia = int(((datetime.date.today() - edad_inscripcion).days)/365)
                existe = Persona.objects.filter(num_identificacion = data_persona['num_identificacion']).count()
                
                if(existe != 0):
                    messages.error(request, "Su Identificacion ya se encuentra registrada")
                    form = PersonaForm(request.POST)
                    form2 = InscripcionForm(request.POST)
                elif(franja == None):
                    messages.error(request, "Por favor seleccione una franja valida")
                    form = PersonaForm(request.POST)
                    form2 = InscripcionForm(request.POST)
                elif(data_persona['email'] == data_persona['email_acudiente']):
                    messages.error(request, "El email de contacto debe ser diferentes al del usuario")
                    form = PersonaForm(request.POST)
                    form2 = InscripcionForm(request.POST)  
                
                elif(data_persona['num_identificacion'] <= 0 or data_persona['tel_contacto'] <= 0 or data_persona['telefono_acudiente'] <= 0 ):
                    messages.error(request, "Por favor revise la información diligenciada.")
                    form = PersonaForm(request.POST)
                    form2 = InscripcionForm(request.POST)
                
                elif(data_persona['tel_contacto'] == data_persona['telefono_acudiente']):
                    messages.error(request, "El número de contacto debe ser diferentes al del usuario")
                    form = PersonaForm(request.POST)
                    form2 = InscripcionForm(request.POST)
                    
                elif(diferencia > 18 and data_persona['tipo_identificacion']==2):
                    messages.error(request, "Su tipo de documento es incorrecto")
                    form = PersonaForm(request.POST)
                    form2 = InscripcionForm(request.POST)
                    
                else: 
                    persona = form.save(commit=False)
                    inscripcion = form2.save(commit=False)
                    if(diferencia < 17):
                        persona.mayor_de_edad = False
                    else:
                        persona.mayor_de_edad = True
                        
                    persona.telefono_acudiente = 0
                    if request.POST.get('solicitud_examen') == 'Deseo presentar examen':
                        inscripcion.sol_examen=True
                    else:
                        inscripcion.sol_examen=False
                    
                        
                    inscripcion.estado_inscripcion=False
                    inscripcion.cita_examen_creada=False
                    user = User.objects.create_user(username=persona.num_identificacion,email=persona.email,password=persona.num_identificacion)
                    persona.usuario = user
                    
                    assign_role(user,'estudiante')
                    form.save()
                    persona_almacenada = Persona.objects.get(num_identificacion=persona.num_identificacion)
                    inscripcion.persona = persona_almacenada
                    inscripcion.numero_consignacion = None
                    franja_seleccionada = Franja.objects.get(id=franja)
                    inscripcion.franja=franja_seleccionada
                    inscripcion.save()
                    
                    return redirect('index')
            except:
                messages.error(request, "Por favor revise la información diligenciada.")
                form = PersonaForm(request.POST)
                form2 = InscripcionForm(request.POST)
        else:
            messages.error(request, "Por favor revise la información diligenciada.")
            form = PersonaForm(request.POST)
            form2 = InscripcionForm(request.POST)
    else:
        form = PersonaForm(request.POST)
        form2 = InscripcionForm(request.POST)
    
    return render(request,'inscripcion/user/inscripcion_form.html',{'form':form, 'form2':form2})
    
def nuevo_idioma_inscripcion(request):
    
    if request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        #recibir los datos
        form = InscripcionForm(request.POST)
        
        if form.is_valid():
            franja = request.POST.get('franja')
            usuario_actual=request.user
            persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
            
            data_inscripcion = form.cleaned_data
            existe = Inscripcion.objects.filter(persona_id=persona_logged.id,idioma_id = data_inscripcion['idioma']).count()
            if(existe != 0):
                messages.error(request, "Usted ya ha realizado esta inscripcion")
                form = InscripcionForm()
            else:    
                inscripcion = form.save(commit=False)
                if request.POST.get('solicitud_examen') == 'Deseo presentar examen':
                    inscripcion.sol_examen=True
                elif request.POST.get('solicitud_examen') == 'No deseo presentar examen':
                    inscripcion.sol_examen=False
                else:
                    messages.error(request, "Por favor revise la información diligenciada")
                    form = InscripcionForm()
                    return render(request,'inscripcion/user/solicitud_nuevo_idioma.html',{'form':form})
                inscripcion.estado_inscripcion=False
                inscripcion.cita_examen_creada=False
                inscripcion.persona = persona_logged
                franja_seleccionada = Franja.objects.get(id=franja)
                inscripcion.franja=franja_seleccionada
                inscripcion.save()    
                return redirect('inscripcion:gestion_inscripciones')
        else:
            messages.error(request, "Por favor revise la información diligenciada.")
            form = InscripcionForm(request.POST)
    else:
        
        form = InscripcionForm()
    
    return render(request,'inscripcion/user/solicitud_nuevo_idioma.html',{'form':form})

"""
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
        traceback.print_exc()
        return render(request,'inscripcion/user/interfaz_continuidad.html')"""
    
"""
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

def gestion_inscripciones(request):
    #Usuario/Persona logged
    if request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    usuario_actual=request.user
    persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)

    solicitudes = Inscripcion.objects.filter(persona=persona_logged).order_by('id')
    contexto ={
        
    }
    contexto['solicitudes'] = solicitudes
    return render(request,'inscripcion/user/gestion_inscripciones.html', contexto)
    
def editar_inscripcion(request, id_inscripcion):
    inscripcion = Inscripcion.objects.get(id=id_inscripcion)
    if request.method == 'GET':
        form = InscripcionForm(instance=inscripcion)
    else:
        form = InscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            franja = request.POST.get('franja')
            usuario_actual=request.user
            persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
            inscripcion = form.save(commit=False)
            data_inscripcion = form.cleaned_data
            
            if request.POST.get('solicitud_examen') == 'Deseo presentar examen':
                inscripcion.sol_examen=True
                solicitud_examen = True
            else:
                inscripcion.sol_examen=False
                solicitud_examen = False
            
            if(franja == None):
                messages.error(request, "Por favor seleccione una franja valida")    
                form = InscripcionForm(instance=inscripcion)
                return render(request, 'inscripcion/user/editar_inscripcion.html', {'form':form})
                
            franja_seleccionada = Franja.objects.get(id=franja)
            inscripcion.franja=franja_seleccionada
            
            existe = Inscripcion.objects.filter(persona_id=persona_logged.id,idioma_id = data_inscripcion['idioma']).exclude(pk=id_inscripcion).count()
            if(existe == 0):
                #inscripcion_antigua = Inscripcion.objects.filter(persona_id=persona_logged.id,idioma_id = data_inscripcion['idioma']).update(sol_examen=solicitud_examen)
                inscripcion.save()
                existe_agenda = Inscripcion_Examen.objects.filter(inscripcion=inscripcion).count()
                if existe_agenda>0:
                    eliminar_agenda = Inscripcion_Examen.objects.filter(inscripcion=inscripcion)
                    eliminar_agenda.delete()
                if solicitud_examen == False:
                    inscripcion.cita_examen_creada = False
                    inscripcion.save()
                else:
                    inscripcion.cita_examen_creada = False
                    inscripcion.save()
                    if inscripcion.estado_inscripcion == True:
                        val = agendar_inscripcion(inscripcion)
                    
                return redirect('inscripcion:gestion_inscripciones')
            else:
                messages.error(request, "Ya ha realizado una inscripcion a este idioma")
                form = InscripcionForm(instance=inscripcion)
    
    return render(request, 'inscripcion/user/editar_inscripcion.html', {'form':form})
    
def eliminar_inscripcion(request, id_inscripcion):
    inscripcion = Inscripcion.objects.get(id=id_inscripcion)
    if request.method =='POST':
        inscripcion.delete()
        return redirect('inscripcion:gestion_inscripciones')
    
    return render(request, 'inscripcion/user/eliminar_inscripcion.html', {'inscripcion':inscripcion})
    
def carga_documentos(request):
    if request.method == 'POST':
        usuario_actual=request.user
        persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
        form = DocumentosForm(request.POST, request.FILES)
        
        if form.is_valid():
            archivo = request.FILES['file_cedula']
            documentos = form.save(commit=False)
            documentos.persona = persona_logged
            documentos.file_cedula = archivo
            documentos.save()
            return HttpResponseRedirect('/index/')
    else:
        form = DocumentosForm()
    return render(request, 'inscripcion/user/documentos_form.html', {'form': form})


from io import BytesIO 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm
import time

def reporte_examenes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Prueba.pdf' 
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)
    #ancho
    c.setLineWidth(.3)
    #tipo de fuente
    c.setFont('Helvetica',22)
    #izquierda-derecha,abajo-arriba
    c.drawString(30,750,'CLC')
    #Cambio de Fuente
    c.setFont('Helvetica-Bold',12)
    c.drawString(30,735,'Centro de Lenguas y Cultura')
    #Fecha
    c.setFont('Helvetica-Bold',12)
    c.drawString(480,750,time.strftime("%d/%m/%Y"))
    
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def confirmar_matriculas(request):
    form = DocumentosForm()
    return render(request,'inscripcion/admin/carga_financiera.html',{'form':form})


#AJAX

from django.views.decorators.csrf import csrf_exempt
import json
#Libreria utilizada para no evaluar el token (Corregir)
@csrf_exempt
def guardar_notas_ajax(request):
    if request.method == 'POST':
        ids = json.loads(request.POST.get('ids'))
        
        notas = json.loads(request.POST.get('notas'))
        niveles = json.loads(request.POST.get('niveles'))
        if notas[0] != None:
            #Validacion de Notas
            for i in range(0, len(ids)):
                if notas[i] == "":
                    Inscripcion_Examen.objects.filter(pk=ids[i]).update(nota=None,nivel_sugerido=niveles[i])
                else:
                    Inscripcion_Examen.objects.filter(pk=ids[i]).update(nota=notas[i],nivel_sugerido=niveles[i])
            return HttpResponse(0)
        else:
            for i in range(0, len(ids)):
                if niveles[i] != "-":
                    Inscripcion_Examen.objects.filter(pk=ids[i]).update(citacion=niveles[i],citacion_enviada=False)
                    
            return HttpResponse(0)
    else:
        return HttpResponse(1)
from django.core import serializers
@csrf_exempt
def get_franjas(request):
    if request.method == 'POST':
        try:
            if request.user.is_anonymous():
                fecha = json.loads(request.POST.get('fecha_nacimiento'))
                fecha_nacimiento = datetime.date(int(fecha[0]), int(fecha[1]), int(fecha[2]))
                diferencia = int(((datetime.date.today() - fecha_nacimiento).days)/365)
            else:
                usuario_actual=request.user
                persona_logged = Persona.objects.get(usuario_id=usuario_actual.id)
                fecha_nacimiento = persona_logged.edad
                diferencia = int(((datetime.date.today() - fecha_nacimiento).days)/365)
                
            id_idioma = request.POST.get('idioma')
            franjas_idioma = Idioma.objects.values_list('franjas').filter(id=id_idioma)
            
            ids =[]
            for identificador in franjas_idioma:
                ids.append(int(identificador[0]))
        
            if diferencia < 17:
                edad = Edad.objects.get(pk=2)
                franjas = Franja.objects.filter(pk__in=ids,edad=edad)
            else:
                edad = Edad.objects.get(pk=1)
                franjas = Franja.objects.filter(pk__in=ids,edad=edad)
            
            
            lista_franjas = []    
            for franja in franjas:
                horarios_list = Franja.objects.values_list('horarios').filter(id=franja.id)
                
                ids = []
                for identificador in horarios_list:
                    ids.append(int(identificador[0]))
                    
                horarios_asignados = Horario.objects.filter(pk__in=ids)
                horarios = []
                for horas in horarios_asignados:
                    obj = {
                        'dia':horas.dia.dia,
                        'inicio':str(horas.hora_inicio),
                        'fin':str(horas.hora_fin),
                    }
                    horarios.append(obj)
                
                obj2={
                    'id':franja.id,
                    'nombre':franja.nombre,
                    'horarios':horarios,
                }
                lista_franjas.append(obj2)
            
            json_p = json.dumps(lista_franjas)
            return HttpResponse(json_p)
        except:    
            traceback.print_exc()
            return HttpResponse(1)
    else:
        return HttpResponse(1)