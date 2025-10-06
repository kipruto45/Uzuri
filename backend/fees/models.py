

from django.db import models
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model

def _get_student_profile_model():
	try:
		return apps.get_model('my_profile', 'StudentProfile')
	except Exception:
		return None

class FeeStructure(models.Model):
	CATEGORY_CHOICES = [
		('tuition', 'Tuition'),
		('hostel', 'Hostel'),
		('library', 'Library'),
		('graduation', 'Graduation'),
		('penalty', 'Penalty'),
	]
	program = models.CharField(max_length=100)
	year = models.PositiveIntegerField()
	semester = models.PositiveIntegerField()
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
	base_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		pass

	def __str__(self):
		return f"{self.program} - Year {self.year} Sem {self.semester} [{self.category}]"

class Invoice(models.Model):

	class Meta:
		indexes = [
			models.Index(fields=['student']),
			models.Index(fields=['status']),
			models.Index(fields=['due_date']),
		]
	STATUS_CHOICES = [
		('unpaid', 'Unpaid'),
		('paid', 'Paid'),
		('partial', 'Partial'),
		('overdue', 'Overdue'),
	]
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
	description = models.CharField(max_length=255)
	category = models.CharField(max_length=20, choices=FeeStructure.CATEGORY_CHOICES, null=True, blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	due_date = models.DateField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Invoice {self.id} - {self.student} - {self.status}"

class Transaction(models.Model):

	class Meta:
		indexes = [
			models.Index(fields=['student']),
			models.Index(fields=['invoice']),
			models.Index(fields=['status']),
			models.Index(fields=['method']),
		]
	METHOD_CHOICES = [
		('mpesa', 'M-Pesa'),
		('airtel', 'Airtel'),
		('bank', 'Bank'),
		('paypal', 'PayPal'),
		('manual', 'Manual'),
	]
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('success', 'Success'),
		('failed', 'Failed'),
		('refunded', 'Refunded'),
	]
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='transactions')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	method = models.CharField(max_length=10, choices=METHOD_CHOICES)
	reference = models.CharField(max_length=100, unique=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Transaction {self.id} - {self.student} - {self.status}"

class Receipt(models.Model):
	transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='receipt', null=True, blank=True)
	pdf_file = models.FileField(upload_to='receipts/', null=True, blank=True)
	qr_code = models.ImageField(upload_to='receipts/qr/', null=True, blank=True)
	digital_signature = models.CharField(max_length=255, null=True, blank=True)
	issued_date = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Receipt {self.id} - {self.transaction}"

class Scholarship(models.Model):
	TYPE_CHOICES = [
		('scholarship', 'Scholarship'),
		('bursary', 'Bursary'),
		('waiver', 'Waiver'),
	]
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scholarships')
	type = models.CharField(max_length=20, choices=TYPE_CHOICES)
	amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.type} for {self.student}"

	def save(self, *args, **kwargs):
		# Keep student as AUTH_USER_MODEL instance to match migrations and tests
		super(Scholarship, self).save(*args, **kwargs)

class AuditTrail(models.Model):
	from django.conf import settings
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	action = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	object_id = models.CharField(max_length=50)
	changes = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.timestamp} - {self.user} - {self.action} {self.model} {self.object_id}"
