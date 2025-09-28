
from django.contrib import admin
from .models import Invoice, Transaction, Receipt, FeeStructure

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ('id', 'student', 'amount', 'due_date', 'status', 'created_at')
	search_fields = ('student__user__username', 'description')
	list_filter = ('status', 'due_date')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('id', 'student', 'invoice', 'amount', 'method', 'reference', 'status', 'created_at')
	search_fields = ('student__user__username', 'reference')
	list_filter = ('method', 'status')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
	list_display = ('id', 'transaction', 'issued_date')
	search_fields = ('transaction__id',)

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
	list_display = ('id', 'program', 'year', 'semester', 'category', 'base_amount', 'created_at')
	search_fields = ('program',)
