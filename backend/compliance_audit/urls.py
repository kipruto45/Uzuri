"""Shim URLConf for compliance_audit.

Placeholder to satisfy include() during development.
"""
from django.urls import path
from django.http import HttpResponse


def _placeholder(request):
	return HttpResponse('compliance_audit placeholder')


urlpatterns = [path('', _placeholder, name='compliance-audit-placeholder')]
