from django.contrib import admin
from .models import DisciplinaryCase, Evidence, Hearing, DisciplinaryAction, Appeal, AuditTrail, DisciplinaryNotification

@admin.register(DisciplinaryCase)
class DisciplinaryCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'status', 'case_type', 'created_at', 'is_active')
    list_filter = ('status', 'is_active', 'case_type')
    search_fields = ('student__user__username', 'case_type', 'description')
    readonly_fields = ('created_at', 'updated_at')

    actions = ['mark_as_resolved', 'send_bulk_notification']

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f"{updated} cases marked as resolved.")
    mark_as_resolved.short_description = "Mark selected cases as resolved"

    def send_bulk_notification(self, request, queryset):
        for case in queryset:
            DisciplinaryNotification.objects.create(case=case, recipient=case.student, message='Bulk admin notification.', channel='in_app')
        self.message_user(request, f"Notifications sent to {queryset.count()} cases.")
    send_bulk_notification.short_description = "Send notification to selected cases"

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'uploaded_by', 'uploaded_at')
    search_fields = ('case__id', 'uploaded_by__username', 'description')
    readonly_fields = ('uploaded_at',)

@admin.register(Hearing)
class HearingAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'scheduled_at', 'location', 'outcome')
    list_filter = ('scheduled_at', 'location')
    search_fields = ('case__id', 'location', 'notes')
    readonly_fields = ('created_at',)

admin.site.register(DisciplinaryAction)
admin.site.register(Appeal)
admin.site.register(AuditTrail)
admin.site.register(DisciplinaryNotification)
