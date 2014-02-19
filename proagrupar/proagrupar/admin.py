from proagrupar.models import Usuario, Projeto, Relatorio
from django.contrib import admin

"""
class UsuarioAdmin(admin.ModelAdmin):
	fields = ('tipo','nome','cpf','siape','email','campus','telefone')
	list_display = ('nome',)
"""
admin.site.register(Usuario)
admin.site.register(Projeto)
admin.site.register(Relatorio)

#admin.site.register(Usuario, UsuarioAdmin)