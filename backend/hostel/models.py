from django.db import models
from my_profile.models import StudentProfile
from fees.models import Invoice

class Hostel(models.Model):
	name = models.CharField(max_length=100, unique=True)
	location = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Room(models.Model):
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
	number = models.CharField(max_length=20)
	capacity = models.PositiveIntegerField()
	current_occupants = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)

	class Meta:
		unique_together = ('hostel', 'number')

	def __str__(self):
		return f"{self.hostel.name} - Room {self.number}"

	@property
	def available(self):
		return self.current_occupants < self.capacity and self.is_active

class HostelApplication(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('approved', 'Approved'),
		('declined', 'Declined'),
	]
	student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='hostel_applications')
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='applications')
	semester = models.CharField(max_length=20)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
	decline_reason = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('student', 'semester')

	def __str__(self):
		return f"{self.student} - {self.room} - {self.semester} - {self.status}"

class RoomAllocation(models.Model):
	student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='room_allocations')
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
	semester = models.CharField(max_length=20)
	application = models.OneToOneField(HostelApplication, on_delete=models.CASCADE, related_name='allocation')
	invoice = models.OneToOneField(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='hostel_allocation')
	allocated_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('student', 'semester')

	def __str__(self):
		return f"{self.student} - {self.room} - {self.semester}"
