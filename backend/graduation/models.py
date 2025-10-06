
from django.db import models
from django.conf import settings

class GraduationEvent(models.Model):
	name = models.CharField(max_length=128)
	date = models.DateField()
	location = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
    
	def __str__(self):
		return f"{self.name} ({self.date})"

class GraduationApplication(models.Model):
	STATUS_CHOICES = [
		("pending", "Pending"),
		("under_review", "Under Review"),
		("approved", "Approved"),
		("rejected", "Rejected"),
		("cleared", "Cleared"),
		("certificate_issued", "Certificate Issued"),
	]
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="graduation_applications")
	event = models.ForeignKey(GraduationEvent, on_delete=models.CASCADE, related_name="applications")
	status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
	remarks = models.TextField(blank=True)
	submitted_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_eligible = models.BooleanField(default=False)
	is_cleared = models.BooleanField(default=False)
	def __str__(self):
		return f"{self.student} - {self.event} ({self.status})"

class GraduationClearance(models.Model):
	application = models.ForeignKey(GraduationApplication, on_delete=models.CASCADE, related_name="clearances")
	department = models.CharField(max_length=128)
	is_cleared = models.BooleanField(default=False)
	cleared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="graduation_clearances")
	remarks = models.TextField(blank=True)
	cleared_at = models.DateTimeField(null=True, blank=True)
	def __str__(self):
		return f"{self.application} - {self.department} ({'Cleared' if self.is_cleared else 'Pending'})"

class GraduationCertificate(models.Model):
	application = models.OneToOneField(GraduationApplication, on_delete=models.CASCADE, related_name="certificate")
	certificate_file = models.FileField(upload_to="graduation_certificates/%Y/%m/%d/", null=True, blank=True)
	issued_at = models.DateTimeField(auto_now_add=True)
	issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="issued_certificates")
	serial_number = models.CharField(max_length=64, unique=True)
	def __str__(self):
		return f"Certificate {self.serial_number} for {self.application.student}"
