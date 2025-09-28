from django.contrib import admin
from .models import MarketplaceItem, Purchase

admin.site.register(MarketplaceItem)
admin.site.register(Purchase)
