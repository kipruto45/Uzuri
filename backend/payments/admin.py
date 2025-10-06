from django.contrib import admin

from .models import (
	PaymentOption, PaymentMethod, PaymentGateway, Payment, PaymentReceipt, PaymentAuditTrail, Refund,
	PaymentNotification, PaymentReversal, PaymentDispute, PaymentSchedule, PaymentIntegrationLog,
	PaymentComment, PaymentAttachment
)

@admin.register(PaymentOption)
class PaymentOptionAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "is_active")
	search_fields = ("name", "category")

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active")
	search_fields = ("name",)

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active")
	search_fields = ("name",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ("user", "amount", "currency", "status", "reference", "created_at")
	search_fields = ("user__email", "reference", "transaction_id")
	list_filter = ("status", "method", "gateway", "currency")
	readonly_fields = ("created_at", "updated_at")

@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
	list_display = ("payment", "receipt_number", "issued_at")
	search_fields = ("receipt_number", "payment__reference")

@admin.register(PaymentAuditTrail)
class PaymentAuditTrailAdmin(admin.ModelAdmin):
	list_display = ("payment", "action", "actor", "timestamp")
	search_fields = ("payment__reference", "action", "actor__email")

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
	list_display = ("payment", "amount", "processed_by", "processed_at", "status")
	search_fields = ("payment__reference", "processed_by__email")

@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
	list_display = ("payment", "recipient", "channel", "sent_at", "is_read")
	search_fields = ("payment__reference", "recipient__email")

@admin.register(PaymentReversal)
class PaymentReversalAdmin(admin.ModelAdmin):
	list_display = ("payment", "reversed_by", "reversed_at")
	search_fields = ("payment__reference", "reversed_by__email")

@admin.register(PaymentDispute)
class PaymentDisputeAdmin(admin.ModelAdmin):
	list_display = ("payment", "user", "status", "created_at", "resolved_at")
	search_fields = ("payment__reference", "user__email")

@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
	list_display = ("user", "amount", "frequency", "next_due", "is_active")
	search_fields = ("user__email",)

@admin.register(PaymentIntegrationLog)
class PaymentIntegrationLogAdmin(admin.ModelAdmin):
	list_display = ("payment", "gateway", "status_code", "created_at")
	search_fields = ("payment__reference", "gateway__name")

@admin.register(PaymentComment)
class PaymentCommentAdmin(admin.ModelAdmin):
	list_display = ("payment", "user", "created_at")
	search_fields = ("payment__reference", "user__email")

@admin.register(PaymentAttachment)
class PaymentAttachmentAdmin(admin.ModelAdmin):
	list_display = ("payment", "uploaded_by", "uploaded_at")
	search_fields = ("payment__reference", "uploaded_by__email")
from django.contrib import admin

# Register your models here.
