from django.contrib import admin
from .models import Invoice, Payment

admin.site.register(Invoice)
admin.site.register(Payment)
