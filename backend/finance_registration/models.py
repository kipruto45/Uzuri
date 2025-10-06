
from django.db import models
from django.conf import settings
from my_profile.models import StudentProfile

# Audit trail model for finance actions
class FinanceAuditTrail(models.Model):
	ACTION_CHOICES = [
		('create', 'Create'),
		('update', 'Update'),
		('approve', 'Approve'),
		('reject', 'Reject'),
		('pay', 'Pay'),
	]
	action = models.CharField(max_length=16, choices=ACTION_CHOICES)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	registration = models.ForeignKey('FinanceRegistration', on_delete=models.CASCADE, null=True, blank=True)
	invoice = models.ForeignKey('FinanceInvoice', on_delete=models.CASCADE, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	details = models.TextField(blank=True)

	def __str__(self):
		return f"{self.action} by {self.user} at {self.timestamp}"

class FinanceInvoice(models.Model):
	registration = models.OneToOneField('FinanceRegistration', on_delete=models.CASCADE, related_name='invoice')
	total_amount = models.DecimalField(max_digits=12, decimal_places=2)
	paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	status = models.CharField(max_length=16, choices=[('unpaid', 'Unpaid'), ('partial', 'Partially Paid'), ('paid', 'Paid')], default='unpaid')
	due_date = models.DateField()
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Invoice {self.id} - {self.status}"


class FinanceCategory(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(blank=True)
	default_amount = models.DecimalField(max_digits=10, decimal_places=2)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class FinanceRegistration(models.Model):
	student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='finance_registrations')
	semester = models.CharField(max_length=16)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=16, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_finance_registrations')
	approved_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.student} - {self.semester}"

class FinanceRegistrationItem(models.Model):
	registration = models.ForeignKey(FinanceRegistration, on_delete=models.CASCADE, related_name='items')
	category = models.ForeignKey(FinanceCategory, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	selected = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.category.name} ({self.amount})"


	def __str__(self):
		return f"Invoice {self.id} - {self.status}"



# Audit trail model for finance actions
