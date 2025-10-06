from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AcademicLeaveRequest, AcademicLeaveApproval, AcademicLeaveDocument, AcademicLeaveAudit
from .serializers import (
	AcademicLeaveRequestSerializer, AcademicLeaveApprovalSerializer,
	AcademicLeaveDocumentSerializer, AcademicLeaveAuditSerializer
)
from notifications.models import Notification
from notifications.tasks import send_notification_task

class AcademicLeaveRequestViewSet(viewsets.ModelViewSet):
	@action(detail=False, methods=['get'], url_path='analytics')
	def analytics(self, request):
		qs = self.get_queryset()
		total_requests = qs.count()
		approved = qs.filter(status='approved').count()
		rejected = qs.filter(status='rejected').count()
		pending = qs.filter(status='pending').count()
		return Response({
			'total_requests': total_requests,
			'approved': approved,
			'rejected': rejected,
			'pending': pending,
		})
	"""
	Academic Leave Request API
	- Students: create, view, edit, cancel own requests
	- Staff/Admin: approve, reject, analytics, view all
	- Notifications: email, in-app, SMS (if available)
	- Analytics: trends, usage stats
	- Security: permissions enforced
	"""

	@action(detail=True, methods=['get'])
	def notifications(self, request, pk=None):
		leave = self.get_object()
		if request.user != leave.student.user and not request.user.is_staff:
			return Response({'error': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
		logs = leave.notification_logs.filter(user=request.user).order_by('-timestamp')
		data = [
			{
				'channel': log.channel,
				'status': log.status,
				'message': log.message,
				'timestamp': log.timestamp,
				'error_message': log.error_message,
			}
			for log in logs
		]
		return Response(data)

	@action(detail=True, methods=['post'])
	def cancel(self, request, pk=None):
		leave = self.get_object()
		if leave.status != 'pending':
			return Response({'error': 'Only pending requests can be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
		if request.user != leave.student.user and not request.user.is_staff:
			return Response({'error': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
		leave.status = 'cancelled'
		leave.save()
		self.send_notification(leave, 'cancelled')
		return Response({'status': 'cancelled'})

	@action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
	def analytics(self, request):
		# Example analytics: count by status, leave type, monthly trends
		from django.db.models import Count
		data = {}
		data['by_status'] = list(self.get_queryset().values('status').annotate(count=Count('id')).order_by('status'))
		data['by_type'] = list(self.get_queryset().values('leave_type').annotate(count=Count('id')).order_by('leave_type'))
		data['monthly'] = list(self.get_queryset().extra(select={'month': "strftime('%Y-%m', start_date)"}).values('month').annotate(count=Count('id')).order_by('month'))
		return Response(data)
	serializer_class = AcademicLeaveRequestSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff or user.is_superuser:
			return AcademicLeaveRequest.objects.all()
		if hasattr(user, 'profile'):
			return AcademicLeaveRequest.objects.filter(student=user.profile)
		return AcademicLeaveRequest.objects.none()

	def perform_create(self, serializer):
		leave = serializer.save()
		Notification.objects.create(
			user=leave.student,
			message='Academic leave request submitted.',
			type='info',
			category='academic_leave',
			channels=['in_app', 'sms', 'email']
		)
		send_notification_task.delay(leave.student.id, 'Academic leave request submitted.')

	@action(detail=True, methods=['post'])
	def submit_document(self, request, pk=None):
		leave = self.get_object()
		serializer = AcademicLeaveDocumentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(leave_request=leave, uploaded_by=request.user)
			Notification.objects.create(
				user=leave.student,
				message='Document uploaded for your academic leave request.',
				type='info',
				category='academic_leave',
				channels=['in_app', 'sms', 'email']
			)
			send_notification_task.delay(leave.student.id, 'Document uploaded for your academic leave request.')
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=True, methods=['post'])
	def approve(self, request, pk=None):
		leave = self.get_object()
		serializer = AcademicLeaveApprovalSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(leave_request=leave, approver=request.user)
			leave.status = 'approved'
			leave.save()
			Notification.objects.create(
				user=leave.student,
				message='Your academic leave request has been approved.',
				type='success',
				category='academic_leave',
				channels=['in_app', 'sms', 'email']
			)
			send_notification_task.delay(leave.student.id, 'Your academic leave request has been approved.')
			return Response({'status': 'approved'})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=True, methods=['post'])
	def reject(self, request, pk=None):
		leave = self.get_object()
		serializer = AcademicLeaveApprovalSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(leave_request=leave, approver=request.user, decision='rejected')
			leave.status = 'rejected'
			leave.save()
			Notification.objects.create(
				user=leave.student,
				message='Your academic leave request has been rejected.',
				type='error',
				category='academic_leave',
				channels=['in_app', 'sms', 'email']
			)
			send_notification_task.delay(leave.student.id, 'Your academic leave request has been rejected.')
			return Response({'status': 'rejected'})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def send_notification(self, leave, status):
		# Real notification logic (email/SMS/in-app) with delivery logging
		from .models import NotificationDeliveryLog
		user = leave.student.user
		subject = f"Academic Leave Request {status.title()}"
		message = f"Dear {user.get_full_name() or user.username}, your academic leave request (ID: {leave.id}) has been {status}."
		# Email
		email_status = 'pending'
		email_error = ''
		try:
			from django.core.mail import send_mail
			send_mail(subject, message, None, [user.email], fail_silently=True)
			email_status = 'delivered'
		except Exception as e:
			email_status = 'failed'
			email_error = str(e)
		NotificationDeliveryLog.objects.create(
			leave_request=leave, user=user, channel='email', status=email_status, message=message, error_message=email_error)
		# In-app
		inapp_status = 'pending'
		inapp_error = ''
		try:
			from my_profile.models import Notification
			Notification.objects.create(user=user, message=message, type='info')
			inapp_status = 'delivered'
		except Exception as e:
			inapp_status = 'failed'
			inapp_error = str(e)
		NotificationDeliveryLog.objects.create(
			leave_request=leave, user=user, channel='in_app', status=inapp_status, message=message, error_message=inapp_error)
		# SMS (if you have SMS integration)
		# Example: send_sms(user.phone, message)
		# Add your SMS logic here if available

class AcademicLeaveApprovalViewSet(viewsets.ModelViewSet):
	queryset = AcademicLeaveApproval.objects.all()
	serializer_class = AcademicLeaveApprovalSerializer
	permission_classes = [permissions.IsAdminUser]

class AcademicLeaveDocumentViewSet(viewsets.ModelViewSet):
	queryset = AcademicLeaveDocument.objects.all()
	serializer_class = AcademicLeaveDocumentSerializer
	permission_classes = [permissions.IsAuthenticated]

class AcademicLeaveAuditViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = AcademicLeaveAudit.objects.all()
	serializer_class = AcademicLeaveAuditSerializer
	permission_classes = [permissions.IsAdminUser]
