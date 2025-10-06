"""Shim URLConf for personalization.

Placeholder to satisfy include() during development.
"""
from django.urls import path
from django.http import HttpResponse


def _placeholder(request):
	return HttpResponse('personalization placeholder')


urlpatterns = [path('', _placeholder, name='personalization-placeholder')]
