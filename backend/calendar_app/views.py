from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import CalendarEvent, CalendarEventAuditLog
from .serializers import CalendarEventSerializer, CalendarEventAuditLogSerializer
from .permissions import IsEventOwnerOrAdmin, IsLecturerOrAdmin
from django.utils import timezone

class CalendarEventViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['get'], url_path='google-auth-url')
    def google_auth_url(self, request):
        from .sync import get_google_auth_url
        url = get_google_auth_url(request.user)
        return Response({'auth_url': url})

    @action(detail=False, methods=['post'], url_path='google-callback')
    def google_callback(self, request):
        from .sync import handle_google_callback
        code = request.data.get('code')
        handle_google_callback(request.user, code)
        return Response({'status': 'Google calendar connected'})

    @action(detail=False, methods=['post'], url_path='push-google')
    def push_google(self, request):
        from .sync import push_events_to_google
        events = self.get_queryset().filter(Q(created_by=request.user) | Q(shared_with=request.user))
        push_events_to_google(request.user, events)
        return Response({'status': 'Events pushed to Google Calendar'})

    @action(detail=False, methods=['get'], url_path='pull-google')
    def pull_google(self, request):
        from .sync import pull_events_from_google
        events = pull_events_from_google(request.user)
        # Optionally, save or merge events
        return Response({'events': events})
    @action(detail=False, methods=['get'], url_path='ical-feed')
    def ical_feed(self, request):
        from .ical_utils import generate_ical_feed
        events = self.get_queryset().filter(Q(created_by=request.user) | Q(shared_with=request.user))
        ical_data = generate_ical_feed(events, request.user)
        from django.http import HttpResponse
        response = HttpResponse(ical_data, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename=uzuri_calendar.ics'
        return response
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
        from .utils import check_event_conflicts
        has_conflict = check_event_conflicts(request.user, start, end)
        return Response({'conflict': has_conflict})

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        from .export import export_events_excel
        events = self.get_queryset().filter(Q(created_by=request.user) | Q(shared_with=request.user))
        output = export_events_excel(events)
        response = Response(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=calendar.xlsx'
        return response

    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        from .export import export_events_pdf
        events = self.get_queryset().filter(Q(created_by=request.user) | Q(shared_with=request.user))
        output = export_events_pdf(events)
        response = Response(output.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=calendar.pdf'
        return response

class CalendarEventAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalendarEventAuditLog.objects.all().select_related('event', 'user')
    serializer_class = CalendarEventAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsLecturerOrAdmin]
