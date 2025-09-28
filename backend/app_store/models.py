from django.db import models
from django.conf import settings

class AppStoreApp(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='apps_developed')
    upload = models.FileField(upload_to='app_store/')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
