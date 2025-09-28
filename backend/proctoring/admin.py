from django.contrib import admin
from .models import ProctoringSession, PlagiarismReport

admin.site.register(ProctoringSession)
admin.site.register(PlagiarismReport)
