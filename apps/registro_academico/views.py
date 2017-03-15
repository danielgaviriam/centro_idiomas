# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import *
from forms import *
from django.http import HttpResponseRedirect
from django.views.generic import ListView

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
        print (str(form.is_valid()))
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = CitacionForm()        
    else:
        form = CitacionForm()
    return render(request,'inscripcion/user/inscripcion_form.html',{'form':form})
    
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

def agendar_citas(request):
    return render(request,'inscripcion/admin/agendar_citas.html')