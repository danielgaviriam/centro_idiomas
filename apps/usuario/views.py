from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from forms import RegistroForm
from models import *
from rolepermissions.shortcuts import assign_role, get_user_role
from centro_idiomas.roles import *    

# Create your views here.
def registro_usuarios(request):
    
    usuario_log = request.user
    role = get_user_role(usuario_log)
    if (role == Estudiante or usuario_log.is_authenticated() == False):
        return HttpResponseRedirect('/index')
    
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        if user_form.is_valid():
            if request.POST.get('permisos') == 'Estudiante':
                usuario = user_form.save(commit=False)
                usuario = User(username=request.POST['username'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                usuario.set_password(request.POST['password1'])
                usuario.save()
                user = User.objects.get(username= request.POST['username'])
                assign_role(user,'estudiante')
                return HttpResponseRedirect('/index')
            elif request.POST.get('permisos') == 'Administrador':
                usuario = user_form.save(commit=False)
                usuario = User(username=request.POST['username'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                usuario.set_password(request.POST['password1'])
                usuario.save()
                user = User.objects.get(username= request.POST['username'])
                assign_role(user,'administrador')
                return HttpResponseRedirect('/index')
        else:
            user_form = RegistroForm()
            roles = Usuario_permisos.objects.all().order_by('id')
    else:
        user_form = RegistroForm()
        roles = Usuario_permisos.objects.all().order_by('id')
        
    contexto = {
        'formulario':user_form,'roles':roles
    }
    return render(request,'usuario/registrar.html',contexto)


from django.views.decorators.csrf import csrf_protect 
from forms import UserAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@csrf_protect
def inicio_sesion(request):
    #Si usario no es anonimo? (ya esta log)
    if not request.user.is_anonymous():
        #Redireccion a Raiz
        return HttpResponseRedirect('/index')
    #Validacion del Formulario a traves del metodo POST
    if request.method == 'POST':
        formulario = UserAuthenticationForm(request.POST)
        
        if formulario.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            acceso_user = authenticate(username = username, password = password)
            # Si el log fue existoso?
            if acceso_user is not None:
                #si el usuario esta activo
                if acceso_user.is_active:
                    #Login
                    login(request,acceso_user)
                    #Redireccion al origen
                    return HttpResponseRedirect('/index')
                else:
                    messages.add_message(request, messages.INFO, 'Error')
            else:
                messages.add_message(request, messages.INFO, 'Por favor revisa tu usuario o password')
        else:
            messages.add_message(request, messages.INFO, 'Error')
    else:
        formulario = UserAuthenticationForm()
        
    contexto = {
        'formulario': formulario
    }

    return render(request,  'login.html', context=contexto)
            

def cerrar_sesion(request):
    if not request.user.is_anonymous():
        logout(request)
        return HttpResponseRedirect('/index/')    
    else:
        return HttpResponseRedirect('/index/')

def index(request):
    return render(request, 'index.html')