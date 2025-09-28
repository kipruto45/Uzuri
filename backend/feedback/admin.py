from django.contrib import admin
from .models import Feedback, Survey, SurveyResponse

admin.site.register(Feedback)
admin.site.register(Survey)
admin.site.register(SurveyResponse)
