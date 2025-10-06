"""Shim URLConf for accessibility_ai.

Placeholder to satisfy include() during development.
"""
from django.urls import path
from django.http import HttpResponse


def _placeholder(request):
	return HttpResponse('accessibility_ai placeholder')


urlpatterns = [path('', _placeholder, name='accessibility-ai-placeholder')]
