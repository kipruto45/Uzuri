from django.db import models
from django.conf import settings

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=32)
