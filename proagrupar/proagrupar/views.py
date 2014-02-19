# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Projeto, Usuario, Relatorio
from proagrupar.forms import FormProjeto, FormUsuario,FormRelatorio, FormAtualizaRelatorio, FormChancelaRelatorio
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from report import write_to_pdf

#=================================================================================================================
#	INÍCIO
#=================================================================================================================
"""
Função que mostra os dados do usuário logado.
"""
@login_required
def index(request):
	usuario = get_object_or_404(Usuario,pk=request.user)
	return render_to_response('index.html',locals(),
		context_instance=RequestContext(request))


"""
Função que mostra as atividades iniciais dos usuarios do sistema
Para os coordenadores envia os projeto filtrados por campus, os relatorios que não foram chancelados
e que tenham sido atualizados.
Para os professores envia os projetos filtrados pelo nome do usuario logado, os relatorios que não
foram atualizados
"""
@login_required
def inicio(request):
	usuario = get_object_or_404(Usuario,pk=request.user)
	projetosC = Projeto.objects.filter(campus = usuario.campus)
	projetosP = Projeto.objects.filter(professor=usuario)
	lista_projetos = []
	lista_relatorios = []
	if usuario.tipo == "COO":
		for proj in projetosC:
			relatorios = Relatorio.objects.filter(projeto=proj)
			cont = 0;
			for rel in relatorios:
				if not rel.chancelamento and rel.descricao != "":
					cont += 1
					lista_relatorios.append(rel)
			if cont != 0:
				lista_projetos.append(proj)
	elif usuario.tipo == "PRO":
		for proj in projetosP:
			relatorios = Relatorio.objects.filter(projeto=proj)
			cont = 0;
			for rel in relatorios:
				if rel.descricao == "":
					cont += 1
					lista_relatorios.append(rel)
			if cont != 0:
				lista_projetos.append(proj)
	"""
	else:
		lista_projetos = Projeto.objects.all()
		lista_relatorios = Relatorio.objects.all()
	"""
	
	return render_to_response("inicio.html",locals(),context_instance=RequestContext(request))

#=================================================================================================================
#	PROJETO
#=================================================================================================================

"""
Função para adicionar novo projeto. O projeto é ligado a um usuário. Somente disponivel para os coordenadores
A view mostra o projeto que foi adicionar e cria os quatro relatorios do projeto.
Os relatórios são de quatro tipos: P1, P2, P3 e FI
Em cada relatório já são fixados as datas de atualização e os tipos de cada um.
"""
@login_required
def adicionaProjeto(request):
	user = get_object_or_404(Usuario,pk=request.user)
	lista_usuarios = []
	usuario = Usuario.objects.all()
	for user in usuario:
		if user.tipo == 'PRO':
			lista_usuarios.append(user)
	if request.method == "POST":
		form = FormProjeto(request.POST)
		if form.is_valid():
			dados = form.cleaned_data
			form.save()
			agora = datetime.date.today()
			proj = get_object_or_404(Projeto,titulo=dados['titulo'])
			proj.campus = user.campus
			proj.save()
			rel1 = Relatorio(projeto=proj,tipo='P1',
				periodoInicio = ((agora+datetime.timedelta(days=90)).strftime('%Y-%m-%d')),
				periodoFim = ((agora+datetime.timedelta(days=105)).strftime('%Y-%m-%d')))
			rel1.save()
			rel2 = Relatorio(projeto=proj,tipo='P2',
				periodoInicio = ((agora+datetime.timedelta(days=180)).strftime('%Y-%m-%d')),
				periodoFim = ((agora+datetime.timedelta(days=195)).strftime('%Y-%m-%d')))
			rel2.save()
			rel3 = Relatorio(projeto=proj,tipo='P3',
				periodoInicio = ((agora+datetime.timedelta(days=270)).strftime('%Y-%m-%d')),
				periodoFim = ((agora+datetime.timedelta(days=285)).strftime('%Y-%m-%d')))
			rel3.save()
			rel4 = Relatorio(projeto=proj,tipo='FI',
				periodoInicio = ((agora+datetime.timedelta(days=360)).strftime('%Y-%m-%d')),
				periodoFim = ((agora+datetime.timedelta(days=375)).strftime('%Y-%m-%d')))
			rel4.save()
			return render_to_response("projetoSalvo.html",{'proj':proj},
		context_instance=RequestContext(request))
	else:
		form = FormProjeto()
	return render_to_response("adicionaProjeto.html",{'form':form,'user':user},
		context_instance=RequestContext(request))

"""
Função que mostra os projetos relacionados aos usuários
Para os professores são mostrados os projetos que tem o seu nome
Para os coordenadores são mostrados os projetos cadastrados pelo campus
Mostra os projetos que não têm todos os relatórios atualizados
"""
@login_required
def projetos(request):
	usuario = get_object_or_404(Usuario,pk=request.user)
	lista_relatorios = []
	hoje = datetime.date.today()
	if usuario.tipo == 'PRO':
		lista_projetos = Projeto.objects.filter(professor=usuario)
		for projeto in lista_projetos:
			relatorios = Relatorio.objects.filter(projeto=projeto)
			for rel in relatorios:
				lista_relatorios.append(rel)
	elif usuario.tipo == 'COO':
		lista_projetos = Projeto.objects.filter(campus=usuario.campus)
		for projeto in lista_projetos:
			relatorios = Relatorio.objects.filter(projeto=projeto)
			for rel in relatorios:
				lista_relatorios.append(rel)
	else:
		projetos = Projeto.objects.all()
	return render_to_response('projetos.html',locals(),
		context_instance=RequestContext(request))

@login_required
def projetosCampus(request,nr_campus):
	lista_projetos = []
	lista_relatorios = []
	if nr_campus == '1':
		projetos = Projeto.objects.filter(campus='AN')
	elif nr_campus == '2':
		projetos = Projeto.objects.filter(campus='CO')
	elif nr_campus == '3':
		projetos = Projeto.objects.filter(campus='FL')
	elif nr_campus == '4':
		projetos = Projeto.objects.filter(campus='PB')
	elif nr_campus == '5':
		projetos = Projeto.objects.filter(campus='PL')
	elif nr_campus == '6':
		projetos = Projeto.objects.filter(campus='PC')
	elif nr_campus == '7':
		projetos = Projeto.objects.filter(campus='PR')
	elif nr_campus == '8':
		projetos = Projeto.objects.filter(campus='SR')
	elif nr_campus == '9':
		projetos = Projeto.objects.filter(campus='TC')
	elif nr_campus == '10':
		projetos = Projeto.objects.filter(campus='TS')
	else:
		projetos = Projeto.objects.filter(campus='UR')
	
	for proj in projetos:
		lista_projetos.append(proj)
	for projeto in lista_projetos:
		relatorios = Relatorio.objects.filter(projeto=projeto)
		for rel in relatorios:
			lista_relatorios.append(rel)

	return render_to_response("projetos.html",locals(),
		context_instance=RequestContext(request))

"""
Função que mostra os dados do projeto clicado
Retorna os relatorios vinculados ao projeto
"""
def projeto(request,nr_projeto):
	projeto = get_object_or_404(Projeto,pk=nr_projeto)
	usuario = get_object_or_404(Usuario,pk=request.user)
	relatorios = Relatorio.objects.filter(projeto=nr_projeto)
	if request.method == "POST":
		form = FormRelatorio(request.POST)
		if form.is_valid():
			form.save()
			return render_to_response('projetoSalvo.html',{},
		context_instance=RequestContext(request))
	else:
		form = FormRelatorio()
	return render_to_response("projeto.html",locals(),
		context_instance=RequestContext(request))

def removeProjeto(request,nr_projeto):
	projeto = get_object_or_404(Projeto,pk=nr_projeto)
	lista_relatorios = Relatorio.objects.filter(projeto=projeto)
	if request.method == "POST":
		for relatorio in lista_relatorios:
			relatorio.delete();
		projeto.delete()
		return render_to_response("removido.html", {},
		context_instance=RequestContext(request))
	else:
		return render_to_response("removeProjeto.html", locals()
			,context_instance=RequestContext(request))

#===================================================================================================================
#		RELATORIO
#===================================================================================================================
"""
Função para adiocinar um novo relatorio
"""
def relatorio(request,nr_projeto,nr_relatorio):
	projeto = get_object_or_404(Projeto,id=nr_projeto)
	relatorio = get_object_or_404(Relatorio,id=nr_relatorio)
	hoje = datetime.date.today()
	if request.method == "POST":
		form = FormAtualizaRelatorio(request.POST)
		if form.is_valid():
			dados = form.cleaned_data
			relatorio.descricao = dados['descricao']
			relatorio.comentario = dados['comentario']
			relatorio.justificativa = dados['justificativa']
			relatorio.save()
			return render_to_response("relatorioSalvo.html",locals(),
		context_instance=RequestContext(request))
	else:
		form = FormAtualizaRelatorio()
	return render_to_response("relatorio.html",locals(),
		context_instance=RequestContext(request))

def relatorioAtualizado(request,nr_relatorio):
	usuario = get_object_or_404(Usuario,pk=request.user)
	relatorio = get_object_or_404(Relatorio,id=nr_relatorio)
	return render_to_response("relatorioAtualizado.html",locals(),
		context_instance=RequestContext(request))

def relatoriosAtualizados(request):
	usuario = get_object_or_404(Usuario,pk=request.user)
	projetos = Projeto.objects.filter(professor=usuario)
	lista_relatorios = []
	for proj in projetos:
		relatorios = Relatorio.objects.filter(projeto=proj)
		for rel in relatorios:
			if rel.descricao != "":
				lista_relatorios.append(rel)
	return render_to_response("relatoriosAtualizados.html",locals(),
		context_instance=RequestContext(request))

@login_required
def relatorios(request):
	usuario = get_object_or_404(Usuario,pk=request.user)
	projetos = Projeto.objects.filter(campus=usuario.campus)
	lista_relatorios = Relatorio.objects.filter(projeto=projetos)
	return render_to_response("relatoriosAtualizados.html",locals(),
		context_instance=RequestContext(request))


def chancela(request,nr_relatorio):
	usuario = get_object_or_404(Usuario,pk=request.user)
	relatorio = get_object_or_404(Relatorio,id=nr_relatorio)
	
	if request.method == "POST":
		form = FormChancelaRelatorio(request.POST,instance=relatorio)
		if form.is_valid():
			form.save()
			return render_to_response("relatorioSalvo.html",{'relatorio':relatorio,'usuario':usuario},
		context_instance=RequestContext(request))
	else:
		form = FormChancelaRelatorio()
	return render_to_response("chancela.html",{'form':form,'relatorio':relatorio,'usuario':usuario}
		,context_instance=RequestContext(request))

def certificados(request):
	lista_certificados = []
	return render_to_response("certificados.html",locals(),context_instance=RequestContext(request))

def relatorio_pdf(request,nr_relatorio):
	usuario = get_object_or_404(Usuario,pk=request.user)
	relatorio = get_object_or_404(Relatorio,pk=nr_relatorio)
	nome = relatorio.projeto
	return write_to_pdf('relatorio.html',locals(),nome)

#===================================================================================================================
#		USUARIO
#===================================================================================================================

def adicionaUsuario(request):
	if request.method == "POST":
		form = FormUsuario(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return render_to_response("usuarioSalvo.html",{},
		context_instance=RequestContext(request))
	else:
		form = FormUsuario()
	return render_to_response("adicionaUsuario.html",locals(),
		context_instance=RequestContext(request))


def professores(request):
	usr = get_object_or_404(Usuario,pk=request.user)
	lista_usuarios = Usuario.objects.filter(tipo="PRO",campus=usr.campus)
	return render_to_response("usuariosCadastrados.html",locals(),
		context_instance=RequestContext(request))


def usuarios(request):
	lista_usuarios = Usuario.objects.all()
	admins = []
	coords = []
	profs = []
	for usr in lista_usuarios:
		if usr.tipo == "ADM":
			admins.append(usr)
		elif usr.tipo == "COO":
			coords.append(usr)
		else:
			profs.append(usr)
	return render_to_response('usuarios.html',locals(),
		context_instance=RequestContext(request))

def usuario(request,nr_usuario):
	usuario = get_object_or_404(Usuario,pk=nr_usuario)
	return render_to_response('usuario.html',locals(),
		context_instance=RequestContext(request))

def editaUsuario(request,nr_usuario):
	usuario = get_object_or_404(Usuario,pk=nr_usuario)
	if request.method == "POST":
		form = FormUsuario(request.POST,instance=usuario)
		if form.is_valid():
			form.save()
			return render_to_response('usuarioSalvo.html',locals(),context_instance=RequestContext(request))
	else:
		form = FormUsuario(instance=usuario)
	return render_to_response("editaUsuario.html",locals(),context_instance=RequestContext(request))

def removeUsuario(request,nr_usuario):
	usuario = get_object_or_404(Usuario,pk=nr_usuario)
	if request.method == "POST":
		usuario.delete()
		return render_to_response("removido.html",{},
		context_instance=RequestContext(request))
	else:
		return render_to_response("removeUsuario.html",locals(),
			context_instance=RequestContext(request))
