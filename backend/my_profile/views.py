"""
my_profile.views

Clean, minimal view implementations used by tests. This file provides the
endpoints the test-suite expects for student profiles and ID card requests.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import mixins

from fees.permissions import IsStudentSelf

from .models import StudentProfile, IDCardReplacementRequest
from .serializers import (
    StudentProfileSerializer,
    IDCardReplacementRequestSerializer,
)
from notifications.models import Notification
from notifications.utils import get_unread_count, get_notification_types, get_delivery_status
from .serializers import NotificationSerializer
import logging
logger = logging.getLogger(__name__)
from rest_framework.views import APIView


class StudentProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def get(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        serializer = StudentProfileSerializer(profile, context={"request": request, "format": None})
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True, context={"request": request, "format": None})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Notification.objects.create(user=request.user, message="Your profile was updated successfully.")
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data, status=status.HTTP_200_OK)


class IDCardRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def post(self, request):
        logger.info("IDCardRequestAPIView called: method=%s, user=%s, authenticated=%s", request.method, getattr(request.user, 'pk', None), request.user.is_authenticated)
        profile = get_object_or_404(StudentProfile, user=request.user)
        reason = request.data.get("reason")
        if not reason:
            return Response({"detail": "Reason required."}, status=400)
        req = IDCardReplacementRequest.objects.create(student=profile, reason=reason)
        Notification.objects.create(user=request.user, message="Your ID replacement request has been submitted for review.")
        serializer = IDCardReplacementRequestSerializer(req)
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data, status=status.HTTP_201_CREATED)


class IDCardDownloadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def get(self, request):
        from .utils import generate_id_card_pdf

        profile = get_object_or_404(StudentProfile, user=request.user)
        if profile.id_card_downloaded:
            Notification.objects.create(user=request.user, message="You have already downloaded your ID. File a replacement request.")
            return Response({"detail": "You’ve already downloaded your ID. File a report to request another."}, status=status.HTTP_403_FORBIDDEN)
        buffer = generate_id_card_pdf(profile)
        profile.id_card_downloaded = True
        profile.save()
        Notification.objects.create(user=request.user, message="Your Student ID card was generated and downloaded.")
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="id_card.pdf"'
        response.status_code = status.HTTP_200_OK
        return response


def get_notification_context(user):
    # Notification model uses `timestamp` for when it was created
    notifications_qs = Notification.objects.filter(user=user).order_by("-timestamp")
    # Serialize notifications so the response is JSON serializable
    notifications = NotificationSerializer(notifications_qs, many=True, context={"request": None}).data
    unread_count = get_unread_count(user)
    notification_types = get_notification_types(user)
    delivery_status = get_delivery_status(user)
    return {
        "notifications": notifications,
        "unread_notification_count": unread_count,
        "notification_types": notification_types,
        "notification_delivery_status": delivery_status,
    }


class StudentProfileViewSet(viewsets.GenericViewSet):
    """Endpoints used by the test-suite for student profiles."""

    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def get_queryset(self):
        return StudentProfile.objects.all()

    def get_object(self):
        return get_object_or_404(StudentProfile, user=self.request.user)

    @action(detail=False, methods=["get"], url_path="", url_name="profile")
    def get_profile(self, request):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch", "put"], url_path="", url_name="profile-update")
    def update_profile(self, request):
        profile = self.get_object()
        partial = request.method == "PATCH"
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.send_in_app_notification(request.user, "Your profile was updated successfully.")
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="id-card/request", url_name="id-card-request")
    def id_card_request(self, request):
        profile = self.get_object()
        reason = request.data.get("reason")
        if not reason:
            return Response({"detail": "Reason required."}, status=400)
        req = IDCardReplacementRequest.objects.create(student=profile, reason=reason)
        self.send_in_app_notification(request.user, "Your ID replacement request has been submitted for review.")
        serializer = IDCardReplacementRequestSerializer(req)
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="id-card", url_name="id-card")
    def id_card(self, request):
        from .utils import generate_id_card_pdf

        profile = self.get_object()
        if profile.id_card_downloaded:
            self.send_in_app_notification(request.user, "You have already downloaded your ID. File a replacement request.")
            return Response({"detail": "You’ve already downloaded your ID. File a report to request another."}, status=status.HTTP_403_FORBIDDEN)
        buffer = generate_id_card_pdf(profile)
        profile.id_card_downloaded = True
        profile.save()
        self.send_in_app_notification(request.user, "Your Student ID card was generated and downloaded.")
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="id_card.pdf"'
        response.status_code = status.HTTP_200_OK
        return response

    def send_in_app_notification(self, user, message):
        Notification.objects.create(user=user, message=message)

    @action(detail=False, methods=["get"], url_path="id-card/requests")
    def id_card_requests(self, request):
        profile = self.get_object()
        requests = profile.id_card_requests.all()
        serializer = IDCardReplacementRequestSerializer(requests, many=True)
        return Response(serializer.data)


class IDCardReplacementRequestAdminViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = IDCardReplacementRequest.objects.filter(status="pending")
    serializer_class = IDCardReplacementRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["patch"], url_path="approve")
    def approve(self, request, pk=None):
        req = self.get_object()
        req.status = "approved"
        req.student.id_card_downloaded = False
        req.student.save()
        req.save()
        return Response({"detail": "Request approved."})

    @action(detail=True, methods=["patch"], url_path="decline")
    def decline(self, request, pk=None):
        req = self.get_object()
        req.status = "declined"
        req.save()
        return Response({"detail": "Request declined."})


