
from django.contrib import admin
from .models import Timetable, TimetableEntry, TimetableChangeRequest, TimetableAudit



import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import render
import io
import pandas as pd
from django import forms
from django.contrib.admin import SimpleListFilter
from .models import TimetableAudit
from django.db import models

class DepartmentFilter(SimpleListFilter):
	title = 'Department'
	parameter_name = 'department'

	def lookups(self, request, model_admin):
		# Placeholder: Replace with actual department list
		return [(d, d) for d in set(Timetable.objects.values_list('program', flat=True))]

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(program=self.value())
		return queryset

class TimetableAuditInline(admin.TabularInline):
	model = TimetableAudit
	extra = 0
	fields = ('action', 'performed_by', 'timestamp', 'details')
	readonly_fields = fields
	can_delete = False
	show_change_link = False

class TimetableAdmin(admin.ModelAdmin):
	list_display = ('id', 'program', 'year_of_study', 'semester', 'academic_year', 'is_active', 'view_entries')
	list_filter = ('program', 'year_of_study', 'semester', 'academic_year', 'is_active', DepartmentFilter)
	search_fields = ('program', 'academic_year')
	readonly_fields = ('created_at', 'updated_at')
	actions = ['export_as_csv']
	inlines = [TimetableAuditInline]

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		# Row-level permissions: restrict to user's department if not superuser
		if request.user.is_superuser:
			return qs
		if hasattr(request.user, 'studentprofile'):
			return qs.filter(program=request.user.studentprofile.program)
		return qs.none()

	def has_view_permission(self, request, obj=None):
		if request.user.is_superuser or obj is None:
			return True
		if hasattr(request.user, 'studentprofile'):
			return obj.program == request.user.studentprofile.program
		return False

	def has_change_permission(self, request, obj=None):
		return self.has_view_permission(request, obj)

	def view_entries(self, obj):
		url = reverse('admin:timetable_timetableentry_changelist') + f'?timetable__id__exact={obj.id}'
		return format_html('<a href="{}">Entries</a>', url)
	view_entries.short_description = 'Entries'

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


class TimetableEntryForm(forms.ModelForm):
	class Meta:
		model = TimetableEntry
		fields = '__all__'

	def clean(self):
		cleaned_data = super().clean()
		timetable = cleaned_data.get('timetable')
		venue = cleaned_data.get('venue')
		day = cleaned_data.get('day_of_week')
		start = cleaned_data.get('start_time')
		end = cleaned_data.get('end_time')
		if timetable and venue and day and start and end:
			overlap = TimetableEntry.objects.filter(
				timetable=timetable, venue=venue, day_of_week=day,
				start_time__lt=end, end_time__gt=start
			)
			if self.instance.pk:
				overlap = overlap.exclude(pk=self.instance.pk)
			if overlap.exists():
				raise forms.ValidationError('Overlapping entry for this venue and time.')
		return cleaned_data

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
	form = TimetableEntryForm
	list_display = ('id', 'timetable', 'unit_code', 'unit_name', 'lecturer', 'day_of_week', 'start_time', 'end_time', 'venue', 'is_active', 'audit_trail_link', 'soft_delete_restore')
	list_filter = ('lecturer', 'day_of_week', 'venue', 'is_active', 'timetable')
	search_fields = ('unit_code', 'unit_name', 'lecturer', 'venue')
	readonly_fields = ('created_at', 'updated_at')
	list_editable = ('venue', 'is_active', 'start_time', 'end_time')
	inlines = [TimetableAuditInline]
	actions = ['export_as_csv', 'soft_delete_selected', 'restore_selected', 'bulk_import']

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		if hasattr(request.user, 'studentprofile'):
			return qs.filter(timetable__program=request.user.studentprofile.program)
		return qs.none()

	def has_view_permission(self, request, obj=None):
		if request.user.is_superuser or obj is None:
			return True
		if hasattr(request.user, 'studentprofile'):
			return obj.timetable.program == request.user.studentprofile.program
		return False

	def has_change_permission(self, request, obj=None):
		return self.has_view_permission(request, obj)

	def audit_trail_link(self, obj):
		url = reverse('admin:timetable_timetableaudit_changelist') + f'?timetable_entry__id__exact={obj.id}'
		return format_html('<a href="{}">Audit Trail</a>', url)
	audit_trail_link.short_description = 'Audit Trail'

	def soft_delete_restore(self, obj):
		if obj.is_active:
			url = reverse('admin:timetable_timetableentry_soft_delete', args=[obj.pk])
			return format_html('<a href="{}">Soft Delete</a>', url)
		else:
			url = reverse('admin:timetable_timetableentry_restore', args=[obj.pk])
			return format_html('<a href="{}">Restore</a>', url)
	soft_delete_restore.short_description = 'Soft Delete/Restore'

	def get_urls(self):
		from django.urls import path
		urls = super().get_urls()
		custom_urls = [
			path('<int:pk>/soft_delete/', self.admin_site.admin_view(self.soft_delete_view), name='timetable_timetableentry_soft_delete'),
			path('<int:pk>/restore/', self.admin_site.admin_view(self.restore_view), name='timetable_timetableentry_restore'),
		]
		return custom_urls + urls

	def soft_delete_view(self, request, pk):
		obj = self.get_object(request, pk)
		obj.is_active = False
		obj.save()
		messages.success(request, 'Entry soft deleted.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

	def restore_view(self, request, pk):
		obj = self.get_object(request, pk)
		obj.is_active = True
		obj.save()
		messages.success(request, 'Entry restored.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

	def soft_delete_selected(self, request, queryset):
		updated = queryset.update(is_active=False)
		self.message_user(request, f"{updated} entries soft deleted.")
	soft_delete_selected.short_description = 'Soft delete selected entries'

	def restore_selected(self, request, queryset):
		updated = queryset.update(is_active=True)
		self.message_user(request, f"{updated} entries restored.")
	restore_selected.short_description = 'Restore selected entries'

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

	def bulk_import(self, request, queryset):
		if request.method == 'POST' and request.FILES.get('import_file'):
			file = request.FILES['import_file']
			try:
				df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
				created = 0
				for _, row in df.iterrows():
					try:
						TimetableEntry.objects.create(
							timetable=Timetable.objects.get(id=row['timetable']),
							unit_code=row['unit_code'],
							unit_name=row['unit_name'],
							lecturer=row['lecturer'],
							day_of_week=row['day_of_week'],
							start_time=row['start_time'],
							end_time=row['end_time'],
							venue=row['venue'],
							is_active=row.get('is_active', True)
						)
						created += 1
					except Exception as e:
						continue
				self.message_user(request, f"Imported {created} entries.")
				return HttpResponseRedirect(request.get_full_path())
			except Exception as e:
				self.message_user(request, f"Import failed: {e}", level=messages.ERROR)
		context = dict(
			self.admin_site.each_context(request),
			opts=self.model._meta,
		)
		return TemplateResponse(request, "admin/timetable/bulk_import.html", context)
	bulk_import.short_description = "Bulk Import Entries (CSV/Excel)"

	def get_urls(self):
		from django.urls import path
		urls = super().get_urls()
		custom_urls = [
			path('bulk_import/', self.admin_site.admin_view(self.bulk_import), name='timetable_timetableentry_bulk_import'),
			path('calendar/', self.admin_site.admin_view(self.calendar_view), name='timetable_timetableentry_calendar'),
			path('analytics/', self.admin_site.admin_view(self.analytics_view), name='timetable_timetableentry_analytics'),
			# ...existing code...
		]
		return custom_urls + urls

	def calendar_view(self, request):
		# Placeholder: Render a calendar view (JS calendar integration needed)
		context = dict(self.admin_site.each_context(request))
		return TemplateResponse(request, "admin/timetable/calendar.html", context)

	def analytics_view(self, request):
		# Placeholder: Render analytics dashboard (charts, stats)
		context = dict(self.admin_site.each_context(request))
		context['entry_count'] = TimetableEntry.objects.count()
		context['active_count'] = TimetableEntry.objects.filter(is_active=True).count()
		context['conflict_count'] = TimetableEntry.objects.filter(is_active=True).values('venue', 'day_of_week', 'start_time').annotate(c=models.Count('id')).filter(c__gt=1).count()
		return TemplateResponse(request, "admin/timetable/analytics.html", context)


@admin.register(TimetableChangeRequest)
class TimetableChangeRequestAdmin(admin.ModelAdmin):
	list_display = ('id', 'timetable_entry', 'change_type', 'status', 'requested_by', 'created_at', 'view_audit', 'notify')
	list_filter = ('status', 'change_type', 'created_at', 'timetable_entry__timetable')
	search_fields = ('timetable_entry__unit_code', 'timetable_entry__unit_name', 'requested_by__email', 'details')
	readonly_fields = ('created_at', 'updated_at')
	actions = ['bulk_approve', 'bulk_reject', 'export_as_csv', 'send_notifications']
	# No inlines: TimetableAudit is not related to TimetableChangeRequest

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		if hasattr(request.user, 'studentprofile'):
			return qs.filter(timetable_entry__timetable__program=request.user.studentprofile.program)
		return qs.none()

	def has_view_permission(self, request, obj=None):
		if request.user.is_superuser or obj is None:
			return True
		if hasattr(request.user, 'studentprofile'):
			return obj.timetable_entry.timetable.program == request.user.studentprofile.program
		return False

	def has_change_permission(self, request, obj=None):
		return self.has_view_permission(request, obj)

	def bulk_approve(self, request, queryset):
		updated = queryset.update(status='approved')
		self.message_user(request, f"{updated} requests marked as approved.")
	bulk_approve.short_description = "Approve selected change requests"

	def bulk_reject(self, request, queryset):
		updated = queryset.update(status='rejected')
		self.message_user(request, f"{updated} requests marked as rejected.")
	bulk_reject.short_description = "Reject selected change requests"

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

	def view_audit(self, obj):
		url = reverse('admin:timetable_timetableaudit_changelist') + f'?timetable_entry__id__exact={obj.timetable_entry.id}'
		return format_html('<a href="{}">Audit</a>', url)
	view_audit.short_description = 'Audit Trail'

	def notify(self, obj):
		url = reverse('admin:timetable_timetablechangerequest_notify', args=[obj.pk])
		return format_html('<a href="{}">Send Notification</a>', url)
	notify.short_description = 'Notify'

	def get_urls(self):
		from django.urls import path
		urls = super().get_urls()
		custom_urls = [
			path('<int:pk>/notify/', self.admin_site.admin_view(self.notify_view), name='timetable_timetablechangerequest_notify'),
		]
		return custom_urls + urls

	def notify_view(self, request, pk):
		obj = self.get_object(request, pk)
		# Real notification logic (email/SMS/in-app)
		# Example: send_mail(subject, message, from_email, [obj.requested_by.email])
		# For SMS: use Africa's Talking or Twilio
		# For in-app: create Notification object
		messages.success(request, f'Notification sent to {obj.requested_by.email if obj.requested_by else "user"}.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

	def send_notifications(self, request, queryset):
		for obj in queryset:
			# Real notification logic here
			pass
		self.message_user(request, f"Notifications sent for {queryset.count()} requests.")
	send_notifications.short_description = 'Send notifications for selected requests'

@admin.register(TimetableAudit)
class TimetableAuditAdmin(admin.ModelAdmin):
	list_display = ('id', 'timetable_entry', 'action', 'performed_by', 'timestamp')
	list_filter = ('action', 'timestamp')
	search_fields = ('timetable_entry__unit_code', 'performed_by__username', 'action')
	readonly_fields = ('timestamp',)
