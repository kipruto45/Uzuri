from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzuri_university.settings')

app = Celery('uzuri_university')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
