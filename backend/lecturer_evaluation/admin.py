from django.contrib import admin
from .models import EvaluationForm, EvaluationResponse, EvaluationSummary

admin.site.register(EvaluationForm)
admin.site.register(EvaluationResponse)
admin.site.register(EvaluationSummary)
