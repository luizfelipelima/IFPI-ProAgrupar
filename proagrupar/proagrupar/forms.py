# -*- coding: utf-8 -*-

from django import forms
from proagrupar.models import Usuario,Projeto,Relatorio

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

class FormUsuario(forms.ModelForm):

	class Meta:
		model = Usuario
		fields = ('username','password','tipo','nome','cpf','siape','campus','email','telefone')

class FormProjeto(forms.ModelForm):
	
	class Meta:
		model = Projeto
		fields = ('professor','titulo')


class FormRelatorio(forms.ModelForm):
	periodoInicio = forms.DateField(
							widget=forms.DateInput(format="%d/%m/%Y"),
							input_formats=['%d/%m/%Y','%d/%m/%y']
						)
	periodoFim = forms.DateField(
							widget=forms.DateInput(format="%d/%m/%Y"),
							input_formats=['%d/%m/%Y','%d/%m/%y']
						)
	
	class Meta:
		model = Relatorio
		fields = ('projeto','tipo','periodoInicio','periodoFim')

class FormAtualizaRelatorio(forms.Form):
	
	descricao = forms.CharField(max_length=1000)
	comentario = forms.CharField(max_length=1000)
	justificativa = forms.CharField(max_length=1000)
	
class FormChancelaRelatorio(forms.ModelForm):
	class Meta:
		model = Relatorio
		fields = ('chancelamento',)