from django.db import models
from django.conf import settings

class Resource(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    available = models.BooleanField(default=True)

class Booking(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resource_bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=32, default='pending')
