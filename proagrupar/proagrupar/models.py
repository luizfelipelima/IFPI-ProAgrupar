# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import re

CAMPUS = (
	(u'AN',u'Angical'),
	(u'CO',u'Corrente'),
	(u'FL',u'Floriano'),
	(u'PB',u'Parnaíba'),
	(u'PL',u'Paulistana'),
	(u'PC',u'Picos'),
	(u'PR',u'Piripiri'),
	(u'SR',u'São Raimundo Nonato'),
	(u'TC',u'Teresina - Central'),
	(u'TS',u'Teresina - Zona Sul'),
	(u'UR',u'Uruçui')
	)

TIPOUSER = (
	(u'ADM',u'Adminstrador'),
	(u'PRO',u'Professor'),
	(u'COO',u'Coodenador')
	)

TIPORELATORIO = (
	(u'P1',u'Parcial 1'),
	(u'P2',u'Parcial 2'),
	(u'P3',u'Parcial 3'),
	(u'FI',u'Final')
	)

class Usuario(User):
	tipo = models.CharField(max_length=3,choices=TIPOUSER)
	nome = models.CharField(max_length=30)
	cpf = models.CharField(max_length=12,unique=True)
	siape = models.CharField(max_length=12,unique=True)
	campus = models.CharField(max_length=2,choices=CAMPUS)
	telefone = models.CharField(max_length=20)

	def __unicode__(self):
		return self.nome

	def save(self):
		r = re.compile('sha1\$.*')
		if not r.match(self.password):
			password = self.password
			self.set_password(password)
		User.save(self)
"""
	def get_absolute_url(self):
		return reverse('proagrupar.views.usuario', args=[str(self.id)])
"""

class Projeto(models.Model):
	professor = models.ForeignKey(Usuario)
	titulo = models.CharField(max_length=200)
	campus = models.CharField(max_length=2,choices=CAMPUS)
	dataEHoraCadastro = models.DateTimeField(auto_now="True")
	
	def __unicode__(self):
		return self.titulo

	def get_absolute_url(self):
		return reverse('proagrupar.views.projeto', args=[str(self.id)])

class Relatorio(models.Model):
	projeto = models.ForeignKey(Projeto)
	tipo = models.CharField(max_length=2,choices=TIPORELATORIO)
	periodoInicio = models.DateField(blank=True)
	periodoFim = models.DateField(blank=True)
	descricao = models.TextField(max_length=1000, blank=True)
	comentario = models.TextField(max_length=1000, blank=True)
	justificativa = models.TextField(max_length=1000, blank=True)
	dataEHoraAtualizacao = models.DateTimeField(auto_now=True,blank = True)	
	dataEHoraChancelamento = models.DateTimeField(auto_now=True,blank = True) 
	chancelamento = models.BooleanField(blank=True)

	def __unicode__(self):
		return self.projeto

	def get_absolute_url(self):
		return reverse('proagrupar.views.projeto', args=[str(self.id)])

class Anexo( models.Model ):
	arquivo = models.FileField( upload_to='uploads/anexos', max_length=500 )
	nome_arquivo = models.CharField( max_length=200, blank=False, null=False )
	relatorio = models.ForeignKey( Relatorio )

	def __unicode__(self):
		return seld.nome_arquivo