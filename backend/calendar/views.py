from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import CalendarEvent, CalendarEventAuditLog
from .serializers import CalendarEventSerializer, CalendarEventAuditLogSerializer
from .permissions import IsEventOwnerOrAdmin, IsLecturerOrAdmin
from django.utils import timezone

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all().select_related('created_by').prefetch_related('shared_with')
    serializer_class = CalendarEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsEventOwnerOrAdmin]

    def perform_create(self, serializer):
        event = serializer.save(created_by=self.request.user)
        CalendarEventAuditLog.objects.create(event=event, action='created', user=self.request.user)
        # TODO: Trigger notifications based on event.notification_settings

    def perform_update(self, serializer):
        event = serializer.save()
        CalendarEventAuditLog.objects.create(event=event, action='updated', user=self.request.user)
        # TODO: Update notifications if needed

    def perform_destroy(self, instance):
        CalendarEventAuditLog.objects.create(event=instance, action='deleted', user=self.request.user)
        instance.delete()

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        now = timezone.now()
        events = CalendarEvent.objects.filter(Q(created_by=request.user) | Q(shared_with=request.user)).filter(end_time__gte=now)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def daily(self, request):
        date = request.query_params.get('date', timezone.now().date())
        events = CalendarEvent.objects.filter(
            Q(created_by=request.user) | Q(shared_with=request.user),
            start_time__date=date
        )
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        start = timezone.now().date()
        end = start + timezone.timedelta(days=7)
        events = CalendarEvent.objects.filter(
            Q(created_by=request.user) | Q(shared_with=request.user),
            start_time__date__gte=start, start_time__date__lte=end
        )
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        start = timezone.now().date().replace(day=1)
        end = (start.replace(month=start.month % 12 + 1, day=1) - timezone.timedelta(days=1))
        events = CalendarEvent.objects.filter(
            Q(created_by=request.user) | Q(shared_with=request.user),
            start_time__date__gte=start, start_time__date__lte=end
        )
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        event = self.get_object()
        user_ids = request.data.get('user_ids', [])
        event.shared_with.add(*user_ids)
        CalendarEventAuditLog.objects.create(event=event, action='shared', user=request.user, details={'shared_with': user_ids})
        return Response({'status': 'event shared'})

    @action(detail=True, methods=['get'])
    def audit_logs(self, request, pk=None):
        event = self.get_object()
        logs = event.audit_logs.all()
        serializer = CalendarEventAuditLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if not start or not end:
            return Response({'error': 'start and end required'}, status=status.HTTP_400_BAD_REQUEST)
        events = CalendarEvent.objects.filter(
            Q(created_by=request.user) | Q(shared_with=request.user),
            start_time__lt=end, end_time__gt=start
        )
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

class CalendarEventAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalendarEventAuditLog.objects.all().select_related('event', 'user')
    serializer_class = CalendarEventAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsLecturerOrAdmin]
