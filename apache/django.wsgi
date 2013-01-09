import os
import sys


sys.path.append('/home/ubuntu/lotr-online')
sys.path.append('/home/ubuntu/lotr-online/django_test')

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_test.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

import monitor
monitor.start(interval=1.0)
