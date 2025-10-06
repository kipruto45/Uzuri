from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Hostel, Room, HostelApplication, RoomAllocation
from .serializers import HostelSerializer, RoomSerializer, HostelApplicationSerializer, RoomAllocationSerializer
from my_profile.models import StudentProfile
from fees.models import Invoice
from django.db import transaction as db_transaction
from django.utils import timezone
from django.db.models import Q
from fees.tasks import send_notification_task

# --- Admin API for Hostel Management ---
class AdminHostelViewSet(viewsets.ViewSet):
	permission_classes = [permissions.IsAdminUser]

	@action(detail=False, methods=['get'], url_path='applications')
	def list_applications(self, request):
		status_filter = request.query_params.get('status')
		qs = HostelApplication.objects.all()
		if status_filter:
			qs = qs.filter(status=status_filter)
		serializer = HostelApplicationSerializer(qs, many=True)
		return Response(serializer.data)

	@action(detail=True, methods=['post'], url_path='approve')
	def approve(self, request, pk=None):
		app = get_object_or_404(HostelApplication, pk=pk, status='pending')
		with db_transaction.atomic():
			room = app.room
			if room.current_occupants >= room.capacity:
				app.status = 'declined'
				app.decline_reason = 'Room is full.'
				app.save()
				send_notification_task.delay(app.student.user.id, f'Your application was declined. Reason: Room is full.')
				return Response({'detail': 'Room is full.'}, status=400)
			app.status = 'approved'
			app.save()
			room.current_occupants += 1
			room.save()
			invoice = Invoice.objects.create(
				student=app.student,
				description=f'Hostel Fee for {room} ({app.semester})',
				category='hostel',
				amount=10000,  # TODO: Make dynamic
				due_date=timezone.now().date(),
				status='unpaid',
			)
			RoomAllocation.objects.create(
				student=app.student,
				room=room,
				semester=app.semester,
				application=app,
				invoice=invoice,
			)
			send_notification_task.delay(app.student.user.id, f'Your hostel application was approved. You have been allocated {room}.')
		return Response({'detail': 'Application approved and room allocated.'})

	@action(detail=True, methods=['post'], url_path='decline')
	def decline(self, request, pk=None):
		reason = request.data.get('reason', 'No reason provided')
		app = get_object_or_404(HostelApplication, pk=pk)
		app.status = 'declined'
		app.decline_reason = reason
		app.save()
		send_notification_task.delay(app.student.user.id, f'Your application was declined. Reason: {reason}')
		return Response({'detail': 'Application declined.'})

	@action(detail=True, methods=['post'], url_path='allocate-override')
	def allocate_override(self, request, pk=None):
		app = get_object_or_404(HostelApplication, pk=pk)
		room = app.room
		with db_transaction.atomic():
			if RoomAllocation.objects.filter(student=app.student, semester=app.semester).exists():
				return Response({'detail': 'Student already allocated for this semester.'}, status=400)
			if room.current_occupants >= room.capacity:
				return Response({'detail': 'Room is full.'}, status=400)
			app.status = 'approved'
			app.save()
			room.current_occupants += 1
			room.save()
			invoice = Invoice.objects.create(
				student=app.student,
				description=f'Hostel Fee for {room} ({app.semester})',
				category='hostel',
				amount=10000,  # TODO: Make dynamic
				due_date=timezone.now().date(),
				status='unpaid',
			)
			RoomAllocation.objects.create(
				student=app.student,
				room=room,
				semester=app.semester,
				application=app,
				invoice=invoice,
			)
			send_notification_task.delay(app.student.user.id, f'You have been manually allocated {room}.')
		return Response({'detail': 'Manual allocation complete.'})
# --- Admin/Automation Logic ---
from fees.tasks import send_notification_task
from django.db.models import Q
from fees.models import Invoice
from django.conf import settings
from celery import shared_task

def approve_hostel_application(app_id, admin_user):
	with db_transaction.atomic():
		app = HostelApplication.objects.select_for_update().get(id=app_id, status='pending')
		room = app.room
		if room.current_occupants >= room.capacity:
			app.status = 'declined'
			app.decline_reason = 'Room is full.'
			app.save()
			send_notification_task.delay(app.student.user.id, f'Your application was declined. Reason: Room is full.')
			return app
		# Approve and allocate
		app.status = 'approved'
		app.save()
		room.current_occupants += 1
		room.save()
		# Generate invoice
		invoice = Invoice.objects.create(
			student=app.student,
			description=f'Hostel Fee for {room} ({app.semester})',
			category='hostel',
			amount=10000,  # TODO: Make dynamic
			due_date=timezone.now().date(),
			status='unpaid',
		)
		alloc = RoomAllocation.objects.create(
			student=app.student,
			room=room,
			semester=app.semester,
			application=app,
			invoice=invoice,
		)
		send_notification_task.delay(app.student.user.id, f'Your hostel application was approved. You have been allocated {room}.')
		return app

def decline_hostel_application(app_id, reason, admin_user):
	app = HostelApplication.objects.get(id=app_id)
	app.status = 'declined'
	app.decline_reason = reason
	app.save()
	send_notification_task.delay(app.student.user.id, f'Your application was declined. Reason: {reason}')
	return app

# --- Background Jobs ---
@shared_task
def mark_unpaid_hostel_invoices_overdue():
	from fees.models import Invoice
	overdue = Invoice.objects.filter(category='hostel', status='unpaid', due_date__lt=timezone.now().date())
	for inv in overdue:
		inv.status = 'overdue'
		inv.save()
		send_notification_task.delay(inv.student.user.id, 'Reminder: Your hostel fee invoice is overdue.')

@shared_task
def send_hostel_fee_reminders():
	from fees.models import Invoice
	reminders = Invoice.objects.filter(category='hostel', status='unpaid', due_date__gt=timezone.now().date())
	for inv in reminders:
		send_notification_task.delay(inv.student.user.id, 'Reminder: Your hostel fee invoice is still unpaid.')
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Hostel, Room, HostelApplication, RoomAllocation
from .serializers import HostelSerializer, RoomSerializer, HostelApplicationSerializer, RoomAllocationSerializer
from my_profile.models import StudentProfile
from fees.models import Invoice
from django.db import transaction as db_transaction
from django.utils import timezone

class StudentHostelViewSet(viewsets.ViewSet):
	permission_classes = [permissions.IsAuthenticated]

	@action(detail=False, methods=['get'], url_path='rooms')
	def rooms(self, request):
		rooms = Room.objects.filter(is_active=True)
		serializer = RoomSerializer(rooms, many=True)
		return Response(serializer.data)

	@action(detail=False, methods=['post'], url_path='apply')
	def apply(self, request):
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		semester = request.data.get('semester')
		room_id = request.data.get('room_id')
		if not semester or not room_id:
			return Response({'detail': 'semester and room_id are required.'}, status=400)
		# Prevent duplicate active applications
		if HostelApplication.objects.filter(student=profile, semester=semester, status__in=['pending', 'approved']).exists():
			return Response({'detail': 'You already have an active application for this semester.'}, status=400)
		room = get_object_or_404(Room, id=room_id, is_active=True)
		if room.current_occupants >= room.capacity:
			return Response({'detail': 'Room is full.'}, status=400)
		with db_transaction.atomic():
			app = HostelApplication.objects.create(student=profile, room=room, semester=semester)
			# Notification stub: send_notification(user, ...)
		return Response({'detail': 'Your hostel application has been submitted.'}, status=201)

	@action(detail=False, methods=['get'], url_path='my-applications')
	def my_applications(self, request):
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		apps = HostelApplication.objects.filter(student=profile).order_by('-created_at')
		serializer = HostelApplicationSerializer(apps, many=True)
		return Response(serializer.data)

	@action(detail=False, methods=['get'], url_path='my-room')
	def my_room(self, request):
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		now_semester = timezone.now().strftime('%Y-%m')
		alloc = RoomAllocation.objects.filter(student=profile, semester=now_semester).first()
		if not alloc:
			return Response({'detail': 'No room allocated for this semester.'}, status=404)
		serializer = RoomAllocationSerializer(alloc)
		return Response(serializer.data)

	@action(detail=False, methods=['get'], url_path='fees')
	def fees(self, request):
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		now_semester = timezone.now().strftime('%Y-%m')
		alloc = RoomAllocation.objects.filter(student=profile, semester=now_semester).first()
		if not alloc or not alloc.invoice:
			return Response({'detail': 'No hostel invoice for this semester.'}, status=404)
		# Use existing Fees module serializer if needed
		return Response({
			'invoice_id': alloc.invoice.id,
			'amount': alloc.invoice.amount,
			'status': alloc.invoice.status,
			'due_date': alloc.invoice.due_date,
		})
