#!/usr/bin/python
import sys, os

sys.path.insert(0, '/var/www/projetos/')

os.chdir('/var/www/projetos/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method='threaded', daemonize='false'
