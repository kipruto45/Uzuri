from django.contrib import admin
from .models import APIToken, APIUsageLog

admin.site.register(APIToken)
admin.site.register(APIUsageLog)
