from django.contrib import admin
from .models import ComplianceRecord, AuditTrail

admin.site.register(ComplianceRecord)
admin.site.register(AuditTrail)
