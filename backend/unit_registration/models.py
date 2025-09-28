# Prerequisite, co-requisite, and capacity checks
def check_prerequisites(student_profile, unit):
	# Example: check if all prerequisite units are passed
	prereqs = unit.prerequisites.all() if hasattr(unit, 'prerequisites') else []
	passed_units = set(student_profile.passed_units.values_list('id', flat=True))
	return all(pr.id in passed_units for pr in prereqs)

def check_corequisites(student_profile, unit, selected_units):
	# Example: check if all co-requisite units are selected
	coreqs = unit.corequisites.all() if hasattr(unit, 'corequisites') else []
	selected_ids = set(u.id for u in selected_units)
	return all(cr.id in selected_ids for cr in coreqs)

def check_unit_capacity(unit):
	# Example: check if unit has available slots
	if hasattr(unit, 'capacity'):
		current = unit.unitregistrationitem_set.count()
		return current < unit.capacity
	return True
# Registration window and add/drop logic
from django.utils import timezone

REGISTRATION_START = None  # Set via admin/config
REGISTRATION_END = None

def is_within_registration_window():
	now = timezone.now().date()
	if REGISTRATION_START and REGISTRATION_END:
		return REGISTRATION_START <= now <= REGISTRATION_END
	return True

def can_add_or_drop():
	return is_within_registration_window()
# Utility and business logic for unit registration
from finance_registration.models import FinanceRegistration
from core.models import Program

def can_register_units(student_profile, semester):
	# Check for approved finance registration for the semester
	reg = FinanceRegistration.objects.filter(student=student_profile, semester=semester, status='approved').first()
	return reg is not None

def get_available_units(student_profile, semester):
	# Validate program, year, semester
	program = getattr(student_profile, 'program', None)
	year = getattr(student_profile, 'year_of_study', None)
	if not program or not year:
		return []
	# Fetch units for program, year, semester
	return Unit.objects.filter(program=program, year=year, semester=semester)

def validate_credit_hours(selected_units):
	total_credits = sum([u.credit_hours for u in selected_units])
	MIN_CREDITS = 12
	MAX_CREDITS = 24
	return MIN_CREDITS <= total_credits <= MAX_CREDITS, total_credits

from django.db import models
from django.conf import settings
from my_profile.models import StudentProfile
from core.models import Unit

class UnitRegistration(models.Model):
	student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='unit_registrations')
	semester = models.CharField(max_length=16)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=16, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_unit_registrations')
	approved_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.student} - {self.semester}"

class UnitRegistrationItem(models.Model):
	registration = models.ForeignKey(UnitRegistration, on_delete=models.CASCADE, related_name='items')
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	selected = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.unit.code} ({self.unit.name})"
