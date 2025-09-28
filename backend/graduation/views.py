
from rest_framework import viewsets, permissions
from .models import GraduationEvent, GraduationApplication, GraduationClearance, GraduationCertificate
from .serializers import (
	GraduationEventSerializer,
	GraduationApplicationSerializer,
	GraduationClearanceSerializer,
	GraduationCertificateSerializer,
)

class GraduationEventViewSet(viewsets.ModelViewSet):
	queryset = GraduationEvent.objects.all()
	serializer_class = GraduationEventSerializer
	permission_classes = [permissions.IsAdminUser]

class GraduationApplicationViewSet(viewsets.ModelViewSet):
	queryset = GraduationApplication.objects.all()
	serializer_class = GraduationApplicationSerializer
	permission_classes = [permissions.IsAuthenticated]

class GraduationClearanceViewSet(viewsets.ModelViewSet):
	queryset = GraduationClearance.objects.all()
	serializer_class = GraduationClearanceSerializer
	permission_classes = [permissions.IsAdminUser]

	def perform_update(self, serializer):
		instance = serializer.save()
		# Business Rule: Notify student once all finance/admin clearance is complete
		application = instance.application
		all_cleared = GraduationClearance.objects.filter(application=application, status='cleared').count() == GraduationClearance.objects.filter(application=application).count()
		if all_cleared:
			from notifications.models import Notification
			Notification.objects.create(
				user=application.student,
				message="Congratulations! All your finance and admin graduation clearances are complete.",
				type="graduation_clearance_complete",
			)
		return instance

class GraduationCertificateViewSet(viewsets.ModelViewSet):
	queryset = GraduationCertificate.objects.all()
	serializer_class = GraduationCertificateSerializer
	permission_classes = [permissions.IsAdminUser]
