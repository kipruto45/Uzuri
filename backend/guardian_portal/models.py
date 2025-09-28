from django.db import models
from django.conf import settings

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_portal_guardian_profile')
    phone = models.CharField(max_length=32)
    email = models.EmailField()

class StudentGuardianLink(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_portal_guardian_links')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='guardian_portal_student_links')
