from django.contrib import admin
from .models import Role, CustomUser, StudentProfile, StudyMode, Disability

admin.site.register(Role)
admin.site.register(CustomUser)
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
	readonly_fields = ('student_id',)
	list_display = ('student_id', 'user', 'program', 'year', 'gpa')
admin.site.register(StudyMode)
admin.site.register(Disability)
