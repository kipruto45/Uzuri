from django.db import models
from django.conf import settings

class MarketplaceItem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    file = models.FileField(upload_to='marketplace/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_items_uploaded')
    created_at = models.DateTimeField(auto_now_add=True)

class Purchase(models.Model):
    item = models.ForeignKey(MarketplaceItem, on_delete=models.CASCADE, related_name='marketplace_purchases')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)
