from django.db import models
from django.conf import settings

class AlumniProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumni_profile')
    graduation_year = models.IntegerField()
    current_position = models.CharField(max_length=128, blank=True)
    bio = models.TextField(blank=True)

class JobPosting(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    company = models.CharField(max_length=128)
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumni_job_postings')
