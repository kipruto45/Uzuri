"""Shim URLConf for alumni_networking.

This is a placeholder so Django can import the include('alumni_networking.urls')
during startup. Replace with real routes when the app is implemented.
"""
from django.urls import path
from django.http import HttpResponse


def _placeholder(request):
	return HttpResponse('alumni_networking placeholder')


urlpatterns = [
	path('', _placeholder, name='alumni-networking-placeholder'),
]
