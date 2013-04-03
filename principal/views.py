from principal.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  AuthenticationForm

# Pagina de inicio
def inicio(request):
	return render_to_response('inicio.html', context_instance=RequestContext(request))

def home(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				user= User.objects.get(username=usuario)
				if acceso.is_active:
					login(request, acceso)
					user.save()
					return HttpResponseRedirect('/')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('home.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def cursos(request):
	cursos_ab = CursoAbierto.objects.all().order_by("fecha_inicio")
	cursos=Curso.objects.all()
	return render_to_response('cursos.html', {'cursos_ab':cursos_ab, 'cursos':cursos}, context_instance=RequestContext(request))

def dato_curso_abierto(request, id_curso_ab):
	dato = CursoAbierto.objects.get(pk=id_curso_ab)
	cursoab = Curso.objects.get(pk=dato.curso_id)
	silabo= Silabo.objects.get(pk=cursoab.silabo_id)
	tema=Tema.objects.filter(silabo=silabo.id)
	subtema=SubTema.objects.all()	
	
	return render_to_response('dato_curso_abierto.html',{'curso_ab':dato, 'curso':cursoab, 'silabo':silabo, 'tema':tema, 'subtema':subtema},context_instance = RequestContext(request))
