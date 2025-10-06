from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Timetable, TimetableEntry, TimetableChangeRequest, TimetableAudit
from .serializers import (
	TimetableSerializer, TimetableEntrySerializer,
	TimetableChangeRequestSerializer, TimetableAuditSerializer
)
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

class TimetableViewSet(viewsets.ModelViewSet):
	queryset = Timetable.objects.all()
	serializer_class = TimetableSerializer
	permission_classes = [permissions.IsAdminUser]

	def perform_update(self, serializer):
		instance = serializer.save()
		# Business Rule: Auto-notification when timetable is updated
		from notifications.models import Notification
		from core.models import CustomUser
		students = CustomUser.objects.filter(is_active=True, is_staff=False)
		for student in students:
			Notification.objects.create(
				user=student,
				message="Timetable has been updated. Please check the latest schedule.",
				type="timetable_update",
			)
		return instance

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		data = serializer.data
		data.update(get_notification_context(request.user))
		return Response(data)

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			data = {"results": serializer.data}
			data.update(get_notification_context(request.user))
			return self.get_paginated_response(data)
		serializer = self.get_serializer(queryset, many=True)
		data = {"results": serializer.data}
		data.update(get_notification_context(request.user))
		return Response(data)

class TimetableEntryViewSet(viewsets.ModelViewSet):
	queryset = TimetableEntry.objects.all()
	serializer_class = TimetableEntrySerializer
	permission_classes = [permissions.IsAuthenticated]

class TimetableChangeRequestViewSet(viewsets.ModelViewSet):
	queryset = TimetableChangeRequest.objects.all()
	serializer_class = TimetableChangeRequestSerializer
	permission_classes = [permissions.IsAuthenticated]

	@action(detail=True, methods=['post'])
	def approve(self, request, pk=None):
		change = self.get_object()
		if change.status != 'pending':
			return Response({'error': 'Not pending.'}, status=status.HTTP_400_BAD_REQUEST)
		change.status = 'approved'
		change.save()
		# Notification logic placeholder
		return Response({'status': 'approved'})

	@action(detail=True, methods=['post'])
	def reject(self, request, pk=None):
		change = self.get_object()
		if change.status != 'pending':
			return Response({'error': 'Not pending.'}, status=status.HTTP_400_BAD_REQUEST)
		change.status = 'rejected'
		change.save()
		# Notification logic placeholder
		return Response({'status': 'rejected'})

class TimetableAuditViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = TimetableAudit.objects.all()
	serializer_class = TimetableAuditSerializer
	permission_classes = [permissions.IsAdminUser]
