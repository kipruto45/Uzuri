from django.contrib import admin
from .models import Result, GradingScale, Recommendation

admin.site.register(Result)
admin.site.register(GradingScale)
admin.site.register(Recommendation)
