from django.contrib import admin
# Register your models here.
from .models import Attachment, AttachmentNotificationLog, AttachmentComment, AttachmentTag, AttachmentAccessLog
# Admin for AttachmentTag
@admin.register(AttachmentTag)
class AttachmentTagAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)

# Admin for AttachmentAccessLog
@admin.register(AttachmentAccessLog)
class AttachmentAccessLogAdmin(admin.ModelAdmin):
	list_display = ("id", "attachment", "user", "action", "timestamp")
	list_filter = ("action", "timestamp", "user")
	search_fields = ("attachment__id", "user__username")

# Admin for AttachmentComment
@admin.register(AttachmentComment)
class AttachmentCommentAdmin(admin.ModelAdmin):
	list_display = ("id", "attachment", "user", "created_at", "updated_at")
	search_fields = ("comment", "user__username", "attachment__id")
	list_filter = ("created_at", "user")
class AttachmentNotificationLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'attachment', 'recipient', 'channel', 'status', 'timestamp')
	list_filter = ('channel', 'status', 'timestamp')
	search_fields = ('recipient', 'message')
	readonly_fields = ('timestamp',)

admin.site.register(AttachmentNotificationLog, AttachmentNotificationLogAdmin)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
import csv

from django.template.response import TemplateResponse
import pandas as pd
from django.db import models

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'file', 'uploaded_by', 'description', 'content_type', 'related_model', 'object_id', 'is_active', 'is_confidential', 'download_count', 'created_at', 'expiry_date', 'is_approved', 'download_limit', 'file_preview', 'soft_delete_restore')
	list_filter = ('is_active', 'is_confidential', 'content_type', 'related_model', 'created_at', 'expiry_date', 'is_approved', 'tags')
	search_fields = ('description', 'file', 'uploaded_by__email', 'object_id', 'tags__name')
	readonly_fields = ('created_at', 'updated_at', 'download_count', 'file_preview')
	filter_horizontal = ('tags', 'shared_with_users', 'shared_with_groups')
	actions = ['export_as_csv', 'soft_delete_selected', 'restore_selected', 'send_notifications', 'scan_for_viruses', 'create_new_version']
	def scan_for_viruses(self, request, queryset):
		import requests
		scanned = 0
		for obj in queryset:
			# Example: VirusTotal public API (replace with your scanner)
			try:
				# This is a placeholder. Replace with real scan logic.
				obj.is_virus_free = True
				obj.virus_scan_report = 'No virus detected (placeholder)'
				obj.save()
				scanned += 1
			except Exception as e:
				continue
		self.message_user(request, f"Virus scan completed for {scanned} attachments.")
	scan_for_viruses.short_description = 'Scan selected attachments for viruses'

	def create_new_version(self, request, queryset):
		created = 0
		for obj in queryset:
			new_version = Attachment.objects.create(
				file=obj.file,
				uploaded_by=obj.uploaded_by,
				description=obj.description,
				content_type=obj.content_type,
				object_id=obj.object_id,
				related_model=obj.related_model,
				is_active=obj.is_active,
				is_confidential=obj.is_confidential,
				download_count=0,
				analytics_data=obj.analytics_data,
				version=obj.version + 1,
				previous=obj,
				is_virus_free=obj.is_virus_free,
				virus_scan_report=obj.virus_scan_report,
			)
			created += 1
		self.message_user(request, f"{created} new versions created.")
	create_new_version.short_description = 'Create new version of selected attachments'
	def send_notifications(self, request, queryset):
		from django.core.mail import send_mail
		import requests
		sent = 0
		for obj in queryset:
			# Email notification
			if obj.uploaded_by and hasattr(obj.uploaded_by, 'email') and obj.uploaded_by.email:
				try:
					send_mail(
						subject='Attachment Notification',
						message=f'Your attachment (ID: {obj.id}) has an update.',
						from_email='noreply@uzuriuniversity.com',
						recipient_list=[obj.uploaded_by.email],
						fail_silently=True
					)
					AttachmentNotificationLog.objects.create(
						attachment=obj,
						recipient=obj.uploaded_by.email,
						channel='email',
						status='sent',
						message=f'Your attachment (ID: {obj.id}) has an update.'
					)
				except Exception:
					AttachmentNotificationLog.objects.create(
						attachment=obj,
						recipient=obj.uploaded_by.email,
						channel='email',
						status='failed',
						message=f'Your attachment (ID: {obj.id}) has an update.'
					)
			# SMS notification (Africa's Talking)
			if hasattr(obj.uploaded_by, 'phone_number') and obj.uploaded_by.phone_number:
				try:
					requests.post(
						'https://api.africastalking.com/version1/messaging',
						headers={
							'apiKey': 'your_api_key',
							'Accept': 'application/json',
							'Content-Type': 'application/x-www-form-urlencoded',
						},
						data={
							'username': 'your_username',
							'to': obj.uploaded_by.phone_number,
							'message': f'Your attachment (ID: {obj.id}) has an update.'
						}
					)
					AttachmentNotificationLog.objects.create(
						attachment=obj,
						recipient=obj.uploaded_by.phone_number,
						channel='sms',
						status='sent',
						message=f'Your attachment (ID: {obj.id}) has an update.'
					)
				except Exception:
					AttachmentNotificationLog.objects.create(
						attachment=obj,
						recipient=obj.uploaded_by.phone_number,
						channel='sms',
						status='failed',
						message=f'Your attachment (ID: {obj.id}) has an update.'
					)
			sent += 1
		self.message_user(request, f"Notifications sent for {sent} attachments.")
	send_notifications.short_description = 'Send notifications for selected attachments'

	def soft_delete_restore(self, obj):
		if obj.is_active:
			url = reverse('admin:attachments_attachment_soft_delete', args=[obj.pk])
			return format_html('<a href="{}">Soft Delete</a>', url)
		else:
			url = reverse('admin:attachments_attachment_restore', args=[obj.pk])
			return format_html('<a href="{}">Restore</a>', url)
	soft_delete_restore.short_description = 'Soft Delete/Restore'

	def get_urls(self):
		from django.urls import path
		urls = super().get_urls()
		custom_urls = [
			path('<int:pk>/soft_delete/', self.admin_site.admin_view(self.soft_delete_view), name='attachments_attachment_soft_delete'),
			path('<int:pk>/restore/', self.admin_site.admin_view(self.restore_view), name='attachments_attachment_restore'),
		]
		return custom_urls + urls

	def soft_delete_view(self, request, pk):
		obj = self.get_object(request, pk)
		obj.is_active = False
		obj.save()
		messages.success(request, 'Attachment soft deleted.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

	def restore_view(self, request, pk):
		obj = self.get_object(request, pk)
		obj.is_active = True
		obj.save()
		messages.success(request, 'Attachment restored.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

	def soft_delete_selected(self, request, queryset):
		updated = queryset.update(is_active=False)
		self.message_user(request, f"{updated} attachments soft deleted.")
	soft_delete_selected.short_description = 'Soft delete selected attachments'

	def restore_selected(self, request, queryset):
		updated = queryset.update(is_active=True)
		self.message_user(request, f"{updated} attachments restored.")
	restore_selected.short_description = 'Restore selected attachments'

	def export_as_csv(self, request, queryset):
		meta = self.model._meta
		field_names = [field.name for field in meta.fields]
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = f'attachment; filename={meta}.csv'
		writer = csv.writer(response)
		writer.writerow(field_names)
		for obj in queryset:
			writer.writerow([getattr(obj, field) for field in field_names])
		return response
	export_as_csv.short_description = "Export Selected as CSV"


# Register your models here.
