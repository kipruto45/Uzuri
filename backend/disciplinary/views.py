from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DisciplinaryCase, Evidence, Hearing, DisciplinaryAction, Appeal, AuditTrail, DisciplinaryNotification
from .serializers import (
    DisciplinaryCaseSerializer, EvidenceSerializer, HearingSerializer,
    DisciplinaryActionSerializer, AppealSerializer, AuditTrailSerializer, NotificationSerializer
)
from my_profile.tasks import send_notification
from notifications.models import Notification
from notifications.tasks import send_notification_task

class IsStudentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'profile') and obj.student == request.user.profile

class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser

class DisciplinaryCaseViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        qs = self.get_queryset()
        total_cases = qs.count()
        resolved = qs.filter(status='resolved').count()
        pending = qs.filter(status='pending').count()
        appeal_count = qs.filter(status='appeal').count()
        return Response({
            'total_cases': total_cases,
            'resolved': resolved,
            'pending': pending,
            'appeals': appeal_count,
        })
    queryset = DisciplinaryCase.objects.all()
    serializer_class = DisciplinaryCaseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['create', 'add_evidence', 'submit_appeal']:
            return [permissions.IsAuthenticated()]
        return [IsStaffOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return DisciplinaryCase.objects.all()
        if hasattr(user, 'profile'):
            return DisciplinaryCase.objects.filter(student=user.profile)
        return DisciplinaryCase.objects.none()

    def perform_create(self, serializer):
        case = serializer.save()
        Notification.objects.create(
            user=case.student,
            message='New disciplinary case created.',
            type='info',
            category='disciplinary',
            channels=['in_app', 'sms', 'email']
        )
        send_notification_task.delay(case.student.id, 'New disciplinary case created.')
        AuditTrail.objects.create(case=case, action='Case created', performed_by=self.request.user)
        DisciplinaryNotification.objects.create(case=case, recipient=case.student.user, message='A new disciplinary case has been opened.', channel='in_app')
        send_notification.delay(case.student.user.email, 'disciplinary_case_created', {'case_id': case.id}, ['email', 'in_app'])

    def perform_update(self, serializer):
        case = serializer.save()
        Notification.objects.create(
            user=case.student,
            message='Your disciplinary case has been updated.',
            type='info',
            category='disciplinary',
            channels=['in_app', 'sms', 'email']
        )
        send_notification_task.delay(case.student.id, 'Your disciplinary case has been updated.')
        AuditTrail.objects.create(case=case, action='Case updated', performed_by=self.request.user)
        DisciplinaryNotification.objects.create(case=case, recipient=case.student.user, message='Your disciplinary case has been updated.', channel='in_app')
        send_notification.delay(case.student.user.email, 'disciplinary_case_updated', {'case_id': case.id}, ['email', 'in_app'])

    @action(detail=True, methods=['post'])
    def add_evidence(self, request, pk=None):
        case = self.get_object()
        serializer = EvidenceSerializer(data=request.data)
        if serializer.is_valid():
            evidence = serializer.save(case=case, uploaded_by=request.user)
            Notification.objects.create(
                user=case.student,
                message='Evidence uploaded to your case.',
                type='info',
                category='disciplinary',
                channels=['in_app', 'sms', 'email']
            )
            send_notification_task.delay(case.student.id, 'Evidence uploaded to your case.')
            AuditTrail.objects.create(case=case, action='Evidence uploaded', performed_by=request.user, details={'evidence_id': evidence.id})
            DisciplinaryNotification.objects.create(case=case, recipient=case.student.user, message='New evidence has been added to your case.', channel='in_app')
            send_notification.delay(case.student.user.email, 'disciplinary_evidence_added', {'case_id': case.id}, ['email', 'in_app'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def submit_appeal(self, request, pk=None):
        case = self.get_object()
        serializer = AppealSerializer(data=request.data)
        if serializer.is_valid():
            appeal = serializer.save(case=case, submitted_by=request.user)
            Notification.objects.create(
                user=case.student,
                message='Appeal submitted for your case.',
                type='info',
                category='disciplinary',
                channels=['in_app', 'sms', 'email']
            )
            send_notification_task.delay(case.student.id, 'Appeal submitted for your case.')
            AuditTrail.objects.create(case=case, action='Appeal submitted', performed_by=request.user, details={'appeal_id': appeal.id})
            DisciplinaryNotification.objects.create(case=case, recipient=case.student.user, message='An appeal has been submitted for your case.', channel='in_app')
            send_notification.delay(case.student.user.email, 'disciplinary_appeal_submitted', {'case_id': case.id}, ['email', 'in_app'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def bulk_resolve(self, request):
        ids = request.data.get('ids', [])
        cases = DisciplinaryCase.objects.filter(id__in=ids)
        updated = cases.update(status='resolved')
        for case in cases:
            Notification.objects.create(
                user=case.student,
                message='Your case has been resolved.',
                type='success',
                category='disciplinary',
                channels=['in_app', 'sms', 'email']
            )
            send_notification_task.delay(case.student.id, 'Your case has been resolved.')
        return Response({'updated': updated, 'detail': f'{updated} cases marked as resolved.'})

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def bulk_notify(self, request):
        ids = request.data.get('ids', [])
        cases = DisciplinaryCase.objects.filter(id__in=ids)
        for case in cases:
            Notification.objects.create(
                user=case.student,
                message='Bulk API notification.',
                type='info',
                category='disciplinary',
                channels=['in_app', 'sms', 'email']
            )
            send_notification_task.delay(case.student.id, 'Bulk API notification.')
        return Response({'notified': cases.count(), 'detail': f'Notifications sent to {cases.count()} cases.'})

class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = [permissions.IsAuthenticated]

class HearingViewSet(viewsets.ModelViewSet):
    queryset = Hearing.objects.all()
    serializer_class = HearingSerializer
    permission_classes = [permissions.IsAuthenticated]

class DisciplinaryActionViewSet(viewsets.ModelViewSet):
    queryset = DisciplinaryAction.objects.all()
    serializer_class = DisciplinaryActionSerializer
    permission_classes = [permissions.IsAuthenticated]

class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuditTrailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditTrail.objects.all()
    serializer_class = AuditTrailSerializer
    permission_classes = [permissions.IsAdminUser]

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DisciplinaryNotification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
