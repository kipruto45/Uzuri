from rest_framework.throttling import UserRateThrottle
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
class RegistrationRateThrottle(UserRateThrottle):
	rate = '10/min'
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def bulk_drop_units(request):
	reg_ids = request.data.get('registration_ids', [])
	unit_id = request.data.get('unit_id')
	for reg_id in reg_ids:
		reg = UnitRegistration.objects.filter(id=reg_id).first()
		if reg:
			item = reg.items.filter(unit_id=unit_id).first()
			if item:
    				item.delete()
	return Response({'detail': f'Bulk dropped unit {unit_id} from registrations.'})

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def bulk_add_units(request):
	reg_ids = request.data.get('registration_ids', [])
	unit_id = request.data.get('unit_id')
	unit = Unit.objects.filter(id=unit_id).first()
	for reg_id in reg_ids:
		reg = UnitRegistration.objects.filter(id=reg_id).first()
		if reg and unit:
			UnitRegistrationItem.objects.create(registration=reg, unit=unit, selected=True)
	return Response({'detail': f'Bulk added unit {unit_id} to registrations.'})
import csv
from django.http import HttpResponse
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def registration_stats(request):
	semester = request.query_params.get('semester')
	regs = UnitRegistration.objects.filter(semester=semester)
	total = regs.count()
	approved = regs.filter(status='approved').count()
	pending = regs.filter(status='pending').count()
	rejected = regs.filter(status='rejected').count()
	return Response({'total': total, 'approved': approved, 'pending': pending, 'rejected': rejected})

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def export_registrations_csv(request):
	semester = request.query_params.get('semester')
	regs = UnitRegistration.objects.filter(semester=semester)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
	writer = csv.writer(response)
	writer.writerow(['Student', 'Semester', 'Status', 'Units'])
	for reg in regs:
		units = ','.join([item.unit.code for item in reg.items.all()])
		writer.writerow([reg.student.user.email, reg.semester, reg.status, units])
	return response
from notifications.models import Notification
from notifications.utils import get_unread_count, get_notification_types, get_delivery_status
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def registration_history(request):
	user = request.user
	profile = get_object_or_404(StudentProfile, user=user)
	regs = UnitRegistration.objects.filter(student=profile).order_by('-created_at')
	data = UnitRegistrationSerializer(regs, many=True).data
	notifications = Notification.objects.filter(user=user).order_by('-created_at')
	unread_count = get_unread_count(user)
	notification_types = get_notification_types(user)
	delivery_status = get_delivery_status(user)
	return Response({
		'history': data,
		'notifications': notifications,
		'unread_notification_count': unread_count,
		'notification_types': notification_types,
		'notification_delivery_status': delivery_status,
	})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_receipt(request, reg_id):
	user = request.user
	profile = get_object_or_404(StudentProfile, user=user)
	reg = get_object_or_404(UnitRegistration, id=reg_id, student=profile)
	# Placeholder: generate PDF or text receipt
	receipt = f"Unit Registration Receipt\nStudent: {profile.user.email}\nSemester: {reg.semester}\nUnits: {[item.unit.code for item in reg.items.all()]}"
	return Response({'receipt': receipt})
def send_deadline_reminders():
	from notifications.models import Notification
	# Example: send reminders to students with pending registrations
	from django.utils import timezone
	today = timezone.now().date()
	# Assume REGISTRATION_END is set
	if REGISTRATION_END and (REGISTRATION_END - today).days <= 3:
		pending_regs = UnitRegistration.objects.filter(status='pending')
		for reg in pending_regs:
			Notification.objects.create(
				user=reg.student.user,
				message=f"Unit registration deadline is approaching!",
				type="unit_registration",
			)
	# Notify admins of pending approvals
	from django.contrib.auth import get_user_model
	User = get_user_model()
	admins = User.objects.filter(is_staff=True)
	for admin in admins:
		Notification.objects.create(
			user=admin,
			message="There are pending unit registrations to approve.",
			type="unit_registration_admin",
		)
from core.models import AuditLog
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_unit(request):
	user = request.user
	profile = get_object_or_404(StudentProfile, user=user)
	reg_id = request.data.get('registration_id')
	unit_id = request.data.get('unit_id')
	registration = get_object_or_404(UnitRegistration, id=reg_id, student=profile)
	if not can_add_or_drop():
		return Response({'error': 'Add/drop period is closed.'}, status=status.HTTP_403_FORBIDDEN)
	unit = get_object_or_404(Unit, id=unit_id)
	UnitRegistrationItem.objects.create(registration=registration, unit=unit, selected=True)
	return Response({'detail': 'Unit added.'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def drop_unit(request):
	user = request.user
	profile = get_object_or_404(StudentProfile, user=user)
	reg_id = request.data.get('registration_id')
	unit_id = request.data.get('unit_id')
	registration = get_object_or_404(UnitRegistration, id=reg_id, student=profile)
	if not can_add_or_drop():
		return Response({'error': 'Add/drop period is closed.'}, status=status.HTTP_403_FORBIDDEN)
	item = get_object_or_404(UnitRegistrationItem, registration=registration, unit_id=unit_id)
	item.delete()
	return Response({'detail': 'Unit dropped.'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unit_dashboard(request):
	user = request.user
	profile = get_object_or_404(StudentProfile, user=user)
	regs = UnitRegistration.objects.filter(student=profile).order_by('-created_at')
	data = UnitRegistrationSerializer(regs, many=True).data
	return Response({'registrations': data})
from core.models import Unit
# Admin/registrar endpoints
class UnitOfferingViewSet(viewsets.ModelViewSet):
	queryset = Unit.objects.all()
	permission_classes = [permissions.IsAdminUser]
	# Add create, update, delete logic as needed

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def bulk_approve_registrations(request):
	ids = request.data.get('ids', [])
	UnitRegistration.objects.filter(id__in=ids, status='pending').update(status='approved', approved_at=timezone.now())
	return Response({'detail': f'Approved {len(ids)} registrations.'})

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def registration_report(request):
	semester = request.query_params.get('semester')
	regs = UnitRegistration.objects.filter(semester=semester)
	data = UnitRegistrationSerializer(regs, many=True).data
	return Response({'registrations': data})

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import UnitRegistration, UnitRegistrationItem, can_register_units, get_available_units, validate_credit_hours, can_add_or_drop, REGISTRATION_END
from .serializers import UnitRegistrationSerializer, UnitRegistrationItemSerializer
from my_profile.models import StudentProfile
from core.models import Unit
from finance_registration.models import FinanceRegistration
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from django.utils import timezone

class UnitRegistrationViewSet(viewsets.ModelViewSet):
	throttle_classes = [RegistrationRateThrottle]
	queryset = UnitRegistration.objects.all()
	serializer_class = UnitRegistrationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return UnitRegistration.objects.all()
		profile = get_object_or_404(StudentProfile, user=user)
		return UnitRegistration.objects.filter(student=profile)

	def create(self, request, *args, **kwargs):
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		semester = request.data.get('semester')
		if not can_register_units(profile, semester):
			# Business Rule: Auto-generate 'Unit Registration Blocked' notification
			from notifications.models import Notification
			Notification.objects.create(
				user=profile.user,
				message="Unit Registration Blocked: You have unpaid fees. Please clear your outstanding balance to proceed.",
				type="unit_registration_blocked",
			)
			return Response({'error': 'You cannot register units because of pending finance registration.'}, status=status.HTTP_403_FORBIDDEN)
		if not can_add_or_drop():
			return Response({'error': 'Unit registration is closed.'}, status=status.HTTP_403_FORBIDDEN)
		units = get_available_units(profile, semester)
		selected_unit_ids = [item['unit'] for item in request.data.get('items', [])]
		selected_units = units.filter(id__in=selected_unit_ids)
		valid, total_credits = validate_credit_hours(selected_units)
		if not valid:
			return Response({'error': f'Credit hours must be between 12 and 24. Selected: {total_credits}'}, status=status.HTTP_400_BAD_REQUEST)
		data = request.data.copy()
		data['student'] = profile.id
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		with db_transaction.atomic():
			registration = serializer.save()
		# Audit log
		AuditLog.objects.create(
			user=profile.user,
			action="unit_registration",
			details=f"Submitted registration for {semester}"
		)
		# Send notification
		from notifications.models import Notification
		Notification.objects.create(
			user=profile.user,
			message=f"Unit registration for {semester} submitted.",
			type="unit_registration",
		)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
	def approve(self, request, pk=None):
		registration = self.get_object()
		registration.status = 'approved'
		registration.approved_by = request.user
		registration.approved_at = timezone.now()
		registration.save()
		# Send notification
		from notifications.models import Notification
		Notification.objects.create(
			user=registration.student.user,
			message=f"Your unit registration for {registration.semester} has been approved.",
			type="unit_registration",
		)
		return Response({'detail': 'Unit registration approved.'})

	@action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
	def reject(self, request, pk=None):
		registration = self.get_object()
		registration.status = 'rejected'
		registration.save()
		# Send notification
		from notifications.models import Notification
		Notification.objects.create(
			user=registration.student.user,
			message=f"Your unit registration for {registration.semester} has been rejected.",
			type="unit_registration",
		)
		return Response({'detail': 'Unit registration rejected.'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_units(request):
	user = request.user
	profile = get_object_or_404(StudentProfile, user=user)
	semester = request.query_params.get('semester')
	units = get_available_units(profile, semester)
	data = [
		{'id': u.id, 'code': u.code, 'name': u.name, 'credit_hours': u.credit_hours}
		for u in units
	]
	return Response({'units': data})
