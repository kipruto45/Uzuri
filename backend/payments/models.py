from django.db import models

# Ensure default payment methods exist
def ensure_default_payment_methods():
    from .models import PaymentMethod
    allowed = ["MPESA", "Airtel Money"]
    # Remove all other payment methods
    PaymentMethod.objects.exclude(name__in=allowed).delete()
    # Ensure only MPESA and Airtel Money exist
    for name in allowed:
        PaymentMethod.objects.get_or_create(name=name, defaults={"is_active": True})

from django.db.models.signals import post_migrate
from django.apps import apps
def create_default_methods(sender, **kwargs):
    if sender.name == "payments":
        ensure_default_payment_methods()
post_migrate.connect(create_default_methods)

class PaymentOption(models.Model):
    CATEGORY_CHOICES = [
		("tuition", "Tuition Fees"),
		("accommodation", "Accommodation/Hostel Fees"),
		("registration", "Registration/Admission Fees"),
		("library", "Library Fees"),
		("examination", "Examination Fees"),
		("graduation", "Graduation Fees"),
		("medical", "Medical/Insurance Fees"),
		("activity", "Activity Fees"),
		("technology", "Technology/ICT Fees"),
		("penalty", "Penalty/Disciplinary Fees"),
		("other", "Other Services"),
	]
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    minimum_percentage_required = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_non_refundable = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class PaymentGateway(models.Model):
    name = models.CharField(max_length=64, unique=True)
    api_key = models.CharField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
		("pending", "Pending"),
		("processing", "Processing"),
		("successful", "Successful"),
		("failed", "Failed"),
		("reversed", "Reversed"),
		("refunded", "Refunded"),
		("disputed", "Disputed"),
	]
    user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="KES")
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    is_non_refundable = models.BooleanField(default=False)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
    reference = models.CharField(max_length=128, unique=True)
    transaction_id = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return f"{self.user} - {self.amount:.2f} {self.currency} ({self.status})"

class PaymentReceipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="receipt")
    receipt_number = models.CharField(max_length=64, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="payment_receipts/%Y/%m/%d/", blank=True, null=True)
    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.payment}"

class PaymentAuditTrail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="audit_trails")
    action = models.CharField(max_length=64)
    actor = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.action} by {self.actor} on {self.payment} at {self.timestamp}"

class Refund(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="refunds")
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	reason = models.TextField(blank=True)
	processed_by = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name="processed_refunds")
	processed_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=32, default="pending")
	def __str__(self):
		return f"Refund {self.amount} for {self.payment}"

class PaymentNotification(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="notifications")
	recipient = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
	message = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True)
	channel = models.CharField(max_length=32, default="system")
	is_read = models.BooleanField(default=False)
	def __str__(self):
		return f"Notification to {self.recipient} for {self.payment}"

class PaymentReversal(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="reversals")
	reason = models.TextField(blank=True)
	reversed_by = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name="reversed_payments")
	reversed_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Reversal for {self.payment}"

class PaymentDispute(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="disputes")
	user = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
	reason = models.TextField()
	status = models.CharField(max_length=32, default="open")
	created_at = models.DateTimeField(auto_now_add=True)
	resolved_at = models.DateTimeField(null=True, blank=True)
	def __str__(self):
		return f"Dispute for {self.payment} by {self.user}"

class PaymentSchedule(models.Model):
	user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name="payment_schedules")
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	frequency = models.CharField(max_length=32)
	next_due = models.DateTimeField()
	is_active = models.BooleanField(default=True)
	metadata = models.JSONField(default=dict, blank=True)
	def __str__(self):
		return f"Schedule for {self.user} - {self.amount} ({self.frequency})"

class PaymentIntegrationLog(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="integration_logs")
	gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True, blank=True)
	request_payload = models.JSONField(default=dict, blank=True)
	response_payload = models.JSONField(default=dict, blank=True)
	status_code = models.CharField(max_length=16, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"IntegrationLog for {self.payment}"


class PaymentCallback(models.Model):
	"""Record provider callback IDs to ensure idempotent processing of webhooks."""
	provider = models.CharField(max_length=64)
	callback_id = models.CharField(max_length=128, unique=True)
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
	payload = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.provider} callback {self.callback_id} for {self.payment}" 

class PaymentComment(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="comments")
	user = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Comment by {self.user} on {self.payment}"

class PaymentAttachment(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="attachments")
	file = models.FileField(upload_to="payment_attachments/%Y/%m/%d/")
	uploaded_by = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	description = models.TextField(blank=True)
	def __str__(self):
		return f"Attachment for {self.payment}"
