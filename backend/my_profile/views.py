from rest_framework import status, permissions
from rest_framework.views import APIView
from notifications.models import Notification
from notifications.utils import get_unread_count, get_notification_types, get_delivery_status


def get_notification_context(user):
	notifications = Notification.objects.filter(user=user).order_by('-timestamp')
	unread_count = get_unread_count(user)
	notification_types = get_notification_types(user)
	delivery_status = get_delivery_status(user)
	return {
		"notifications": notifications,
		"unread_notification_count": unread_count,
		"notification_types": notification_types,
		"notification_delivery_status": delivery_status,
	}


class IsStudentSelf(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.user == request.user


class StudentProfileAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

	def get(self, request):
		profile = get_object_or_404(StudentProfile, user=request.user)
		serializer = StudentProfileSerializer(profile)
		data = serializer.data
		data.update(get_notification_context(request.user))
		return Response(data, status=status.HTTP_200_OK)

	def patch(self, request):
		profile = get_object_or_404(StudentProfile, user=request.user)
		serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		Notification.objects.create(user=request.user, message="Your profile was updated successfully.")
		data = serializer.data
		data.update(get_notification_context(request.user))
		return Response(data, status=status.HTTP_200_OK)

	def put(self, request):
		profile = get_object_or_404(StudentProfile, user=request.user)
		serializer = StudentProfileSerializer(profile, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		Notification.objects.create(user=request.user, message="Your profile was updated successfully.")
		data = serializer.data
		data.update(get_notification_context(request.user))
		return Response(data, status=status.HTTP_200_OK)

class IDCardRequestAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

	def post(self, request):
		profile = get_object_or_404(StudentProfile, user=request.user)
		reason = request.data.get('reason')
		if not reason:
			return Response({'detail': 'Reason required.'}, status=400)
		req = IDCardReplacementRequest.objects.create(student=profile, reason=reason)
		Notification.objects.create(user=request.user, message="Your ID replacement request has been submitted for review.")
		serializer = IDCardReplacementRequestSerializer(req)
		data = serializer.data
		data.update(get_notification_context(request.user))
		return Response(data, status=status.HTTP_201_CREATED)
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import StudentProfile, IDCardReplacementRequest, Notification, LoginActivity
from .serializers import StudentProfileSerializer, IDCardReplacementRequestSerializer, NotificationSerializer, LoginActivitySerializer
from django.contrib.auth import get_user_model
from django.conf import settings
import io
import csv

class IsStudentSelf(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.user == request.user

class StudentProfileViewSet(viewsets.GenericViewSet):
	queryset = StudentProfile.objects.all()
	serializer_class = StudentProfileSerializer
	permission_classes = [permissions.IsAuthenticated, IsStudentSelf]
	queryset = StudentProfile.objects.all()
	serializer_class = StudentProfileSerializer
	permission_classes = [permissions.IsAuthenticated, IsStudentSelf]
	@action(detail=False, methods=['get'], url_path='', url_name='profile')
	def get_profile(self, request):
		profile = self.get_object()
		serializer = self.get_serializer(profile)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(detail=False, methods=['put', 'patch'], url_path='', url_name='profile-update')
	def update_profile(self, request):
		profile = self.get_object()
		partial = request.method == 'PATCH'
		serializer = self.get_serializer(profile, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		self.send_in_app_notification(request.user, "Your profile was updated successfully.")
		return Response(serializer.data, status=status.HTTP_200_OK)
	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		self.send_in_app_notification(request.user, "Your profile was updated successfully.")
		return Response(serializer.data, status=status.HTTP_200_OK)
	@action(detail=False, methods=['get'], url_path='export-profile-csv')
	def export_profile_csv(self, request):
		profile = StudentProfile.objects.get(user=request.user)
		notifications = Notification.objects.filter(user=request.user)
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="profile_and_notifications.csv"'
		writer = csv.writer(response)
		writer.writerow(['Profile Field', 'Value'])
		for field in ['user', 'program', 'year_of_study', 'dob', 'gender', 'phone', 'address', 'emergency_contact', 'profile_photo', 'id_card_downloaded', 'created_at', 'updated_at', 'registration_date', 'last_login', 'account_status']:
			writer.writerow([field, getattr(profile, field, '')])
		writer.writerow([])
		writer.writerow(['Notifications'])
		writer.writerow(['Message', 'Type', 'Link', 'Is Read', 'Created At'])
		for n in notifications:
			writer.writerow([n.message, n.type, n.link, n.is_read, n.created_at])
		return response
	def send_in_app_notification(self, user, message):
		Notification.objects.create(user=user, message=message)

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.user != request.user:
			return Response({
				'error': 'Permission denied.',
				'detail': 'You can only update your own profile.'
			}, status=status.HTTP_403_FORBIDDEN)
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		self.send_in_app_notification(request.user, "Your profile was updated successfully.")
		return Response(serializer.data, status=status.HTTP_200_OK)
	serializer_class = StudentProfileSerializer
	permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

	def get_object(self):
		return get_object_or_404(StudentProfile, user=self.request.user)
	def post(self, request):
		import logging
		logging.warning('DEBUG: id_card_request called')
		profile = self.get_object()
		reason = request.data.get('reason')
		if not reason:
			return Response({'detail': 'Reason required.'}, status=400)
		req = IDCardReplacementRequest.objects.create(student=profile, reason=reason)
		self.send_in_app_notification(request.user, "Your ID replacement request has been submitted for review.")
		return Response({'detail': 'Your request has been submitted. Await admin approval.'}, status=201)

	def id_card(self, request):
		from .utils import generate_id_card_pdf
		profile = self.get_object()
		if profile.id_card_downloaded:
			self.send_in_app_notification(request.user, "You have already downloaded your ID. File a replacement request.")
			return Response({'detail': "You’ve already downloaded your ID. File a report to request another."}, status=status.HTTP_403_FORBIDDEN)
		buffer = generate_id_card_pdf(profile)
		profile.id_card_downloaded = True
		profile.save()
		self.send_in_app_notification(request.user, "Your Student ID card was generated and downloaded.")
		response = HttpResponse(buffer, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="id_card.pdf"'
		response.status_code = status.HTTP_200_OK
		return response
		from .utils import generate_id_card_pdf
		profile = self.get_object()
		if profile.id_card_downloaded:
			self.send_in_app_notification(request.user, "You have already downloaded your ID. File a replacement request.")
			return Response({'detail': "You’ve already downloaded your ID. File a report to request another."}, status=status.HTTP_403_FORBIDDEN)
		buffer = generate_id_card_pdf(profile)
		profile.id_card_downloaded = True
		profile.save()
		self.send_in_app_notification(request.user, "Your Student ID card was generated and downloaded.")
		response = HttpResponse(buffer, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="id_card.pdf"'
		response.status_code = status.HTTP_200_OK
		return response

	@action(detail=False, methods=['post'], url_path='id-card/request', url_name='id-card-request')
	def id_card_request(self, request):
		profile = self.get_object()
		reason = request.data.get('reason')
		if not reason:
			return Response({'detail': 'Reason required.'}, status=400)
		req = IDCardReplacementRequest.objects.create(student=profile, reason=reason)
		self.send_in_app_notification(request.user, "Your ID replacement request has been submitted for review.")
		serializer = IDCardReplacementRequestSerializer(req)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	@action(detail=False, methods=['get'], url_path='id-card', url_name='id-card')
	def id_card(self, request):
		from .utils import generate_id_card_pdf
		profile = self.get_object()
		if profile.id_card_downloaded:
			self.send_in_app_notification(request.user, "You have already downloaded your ID. File a replacement request.")
			return Response({'detail': "You’ve already downloaded your ID. File a report to request another."}, status=status.HTTP_403_FORBIDDEN)
		buffer = generate_id_card_pdf(profile)
		profile.id_card_downloaded = True
		profile.save()
		self.send_in_app_notification(request.user, "Your Student ID card was generated and downloaded.")
		response = HttpResponse(buffer, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="id_card.pdf"'
		response.status_code = status.HTTP_200_OK
		return response

	@action(detail=False, methods=['get'], url_path='id-card/requests')
	def id_card_requests(self, request):
		profile = self.get_object()
		requests = profile.id_card_requests.all()
		serializer = IDCardReplacementRequestSerializer(requests, many=True)
		return Response(serializer.data)

class IDCardReplacementRequestAdminViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
	queryset = IDCardReplacementRequest.objects.filter(status='pending')
	serializer_class = IDCardReplacementRequestSerializer
	permission_classes = [permissions.IsAdminUser]

	@action(detail=True, methods=['patch'], url_path='approve')
	def approve(self, request, pk=None):
		req = self.get_object()
		req.status = 'approved'
		req.student.id_card_downloaded = False
		req.student.save()
		req.save()
		# TODO: Trigger notification
		return Response({'detail': 'Request approved.'})

	@action(detail=True, methods=['patch'], url_path='decline')
	def decline(self, request, pk=None):
		req = self.get_object()
		req.status = 'declined'
		req.save()
		# TODO: Trigger notification
		return Response({'detail': 'Request declined.'})

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user).order_by('-created_at')
        notif_type = self.request.query_params.get('type')
        if notif_type:
            queryset = queryset.filter(type=notif_type)
        return queryset

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'})

    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request):
        Notification.objects.filter(user=request.user).delete()
        return Response({'detail': 'All notifications deleted.'})

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read.'})

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_notification(self, request, pk=None):
        notification = self.get_object()
        notification.delete()
        return Response({'detail': 'Notification deleted.'})


class AdminNotificationViewSet(viewsets.ModelViewSet):
	"""CRUD for admin notifications (placeholder, customize as needed)."""
	# TODO: Replace with actual AdminNotification model and serializer if available
	queryset = Notification.objects.filter(type='admin').order_by('-created_at')
	serializer_class = NotificationSerializer
	permission_classes = [permissions.IsAdminUser]

class LoginActivityViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = LoginActivity.objects.all()
	serializer_class = LoginActivitySerializer
	permission_classes = [permissions.IsAuthenticated]


