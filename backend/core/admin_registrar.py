from django.contrib import admin
from .models_registrar import *

@admin.register(RegistrarProfile)
class RegistrarProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role')

@admin.register(Disability)
class DisabilityAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'support_needs', 'tagged_for_reporting')
    list_filter = ('category', 'tagged_for_reporting')
    search_fields = ('student__user__email',)

@admin.register(StudyMode)
class StudyModeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(StudentAdmission)
class StudentAdmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'intake_year', 'program', 'campus', 'department', 'study_mode')
    search_fields = ('student__user__email', 'program', 'campus', 'department')

@admin.register(LeaveOfAbsence)
class LeaveOfAbsenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'requested_at', 'approved_at', 'approved_by')
    list_filter = ('status',)
    search_fields = ('student__user__email',)

@admin.register(TransferRequest)
class TransferRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_program', 'to_program', 'status', 'requested_at', 'approved_at', 'approved_by')
    list_filter = ('status',)
    search_fields = ('student__user__email', 'from_program', 'to_program')

@admin.register(GraduationClearance)
class GraduationClearanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'checked_at', 'checked_by')
    list_filter = ('status',)
    search_fields = ('student__user__email',)

@admin.register(RegistrarAuditLog)
class RegistrarAuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'encrypted')
    search_fields = ('user__email', 'action')
