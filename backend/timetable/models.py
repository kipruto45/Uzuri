
from django.db import models
from django.conf import settings
from django.utils import timezone

class Timetable(models.Model):
	SEMESTER_CHOICES = [
		('semester_1', 'Semester 1'),
		('semester_2', 'Semester 2'),
		('trimester_1', 'Trimester 1'),
		('trimester_2', 'Trimester 2'),
		('trimester_3', 'Trimester 3'),
	]
	program = models.CharField(max_length=100, db_index=True)
	year_of_study = models.PositiveIntegerField(db_index=True)
	semester = models.CharField(max_length=32, choices=SEMESTER_CHOICES, db_index=True)
	academic_year = models.CharField(max_length=16, db_index=True)
	is_active = models.BooleanField(default=True, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
	updated_at = models.DateTimeField(auto_now=True)
	analytics_data = models.JSONField(default=dict, blank=True)

	def __str__(self):
		return f"{self.program} Y{self.year_of_study} {self.semester} {self.academic_year}"

class TimetableEntry(models.Model):
	timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='entries')
	unit_code = models.CharField(max_length=16, db_index=True)
	unit_name = models.CharField(max_length=128)
	lecturer = models.CharField(max_length=128, db_index=True)
	day_of_week = models.CharField(max_length=16, db_index=True)
	start_time = models.TimeField(db_index=True)
	end_time = models.TimeField(db_index=True)
	venue = models.CharField(max_length=128, db_index=True)
	is_active = models.BooleanField(default=True, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class TimetableChangeRequest(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
		('cancelled', 'Cancelled'),
		('completed', 'Completed'),
	]
	timetable_entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE, related_name='change_requests')
	requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	change_type = models.CharField(max_length=32, db_index=True)  # e.g., reschedule, venue change
	details = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
	updated_at = models.DateTimeField(auto_now=True)

class TimetableAudit(models.Model):
	timetable_entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE, related_name='audit_trail')
	action = models.CharField(max_length=255)
	performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_audittrail')
	timestamp = models.DateTimeField(auto_now_add=True)
	details = models.JSONField(default=dict, blank=True)
