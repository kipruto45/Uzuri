import os, sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzuri_university.settings')
import django
django.setup()
from django.urls import resolve

path = '/api/notifications/analytics/'
try:
    match = resolve(path)
    print('Resolved view func:', match.func)
    print('View name:', match.view_name)
    print('Namespace:', match.namespace)
    print('Args:', match.args)
    print('Kwargs:', match.kwargs)
except Exception as e:
    print('Resolve error:', e)
