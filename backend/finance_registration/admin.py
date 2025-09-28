from django.contrib import admin
from .models import FinanceCategory, FinanceRegistration, FinanceRegistrationItem, FinanceInvoice, FinanceAuditTrail
@admin.register(FinanceAuditTrail)
class FinanceAuditTrailAdmin(admin.ModelAdmin):
	list_display = ('action', 'user', 'registration', 'invoice', 'timestamp')
	list_filter = ('action', 'user')

@admin.register(FinanceCategory)
class FinanceCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'default_amount', 'is_active')
	search_fields = ('name',)

@admin.register(FinanceRegistration)
class FinanceRegistrationAdmin(admin.ModelAdmin):
	list_display = ('student', 'semester', 'status', 'created_at', 'approved_by', 'approved_at')
	list_filter = ('semester', 'status')
	search_fields = ('student__user__email',)

@admin.register(FinanceRegistrationItem)
class FinanceRegistrationItemAdmin(admin.ModelAdmin):
	list_display = ('registration', 'category', 'amount', 'selected')
	list_filter = ('category', 'selected')

@admin.register(FinanceInvoice)
class FinanceInvoiceAdmin(admin.ModelAdmin):
	list_display = ('registration', 'total_amount', 'paid_amount', 'status', 'due_date')
	list_filter = ('status',)
