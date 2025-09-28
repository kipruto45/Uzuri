from django.db import models
from django.conf import settings

class BlockchainCredential(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blockchain_credentials')
    credential_type = models.CharField(max_length=64)
    data = models.JSONField(default=dict)
    issued_at = models.DateTimeField(auto_now_add=True)
    blockchain_tx = models.CharField(max_length=128, blank=True)
