from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'projetos.views.home', name='home'),
    # url(r'^projetos/', include('projetos.foo.urls')),
    (r'^$','proagrupar.views.index'),
    (r'^inicio/$','proagrupar.views.inicio'),
    (r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login2.html' }),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login',{'login_url': '/login/?next=/'}),

    #============= USUARIO =============================
    (r'^adicionaUsuario/$','proagrupar.views.adicionaUsuario'),
    (r'^professores/$','proagrupar.views.professores'),
    (r'^usuarios/$','proagrupar.views.usuarios'),
    (r'^usuario/(?P<nr_usuario>\d+)/$','proagrupar.views.usuario'),
    (r'^removeUsuario/(?P<nr_usuario>\d+)/$', 'proagrupar.views.removeUsuario'),
    (r'^editaUsuario/(?P<nr_usuario>\d+)/$','proagrupar.views.editaUsuario'),

    #============= PROJETO =============================
    (r'^adicionaProjeto/$','proagrupar.views.adicionaProjeto'),
    (r'^projetos/$','proagrupar.views.projetos'),
    (r'^projetosCampus/(?P<nr_campus>\d+)/$','proagrupar.views.projetosCampus'),
    (r'^projeto/(?P<nr_projeto>\d+)/$','proagrupar.views.projeto'),
    (r'removeProjeto/(?P<nr_projeto>\d+)/$', 'proagrupar.views.removeProjeto'),

    #============= RELATORIO ===========================
    (r'^relatorios/$','proagrupar.views.relatorios'),
    (r'^relatoriosAtualizados/$','proagrupar.views.relatoriosAtualizados'),
    (r'^relatorioAtualizado/(?P<nr_relatorio>\d+)/$','proagrupar.views.relatorioAtualizado'),
    (r'^relatorio/(?P<nr_projeto>\d+)/(?P<nr_relatorio>\d+)/$','proagrupar.views.relatorio'),
    (r'^chancela/(?P<nr_relatorio>\d+)/$','proagrupar.views.chancela'),
    (r'^certificados/$','proagrupar.views.certificados'),
    (r'^relatorio_pdf/(?P<nr_relatorio>\d+)/$','proagrupar.views.relatorio_pdf'),
    
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$','django.views.static.serve',
			{'document_root':settings.MEDIA_ROOT}),
	)
