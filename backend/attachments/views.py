from django.db import models
from rest_framework import viewsets, permissions, throttling, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attachment, AttachmentComment, AttachmentTag, AttachmentAccessLog
from .serializers import AttachmentSerializer, AttachmentCommentSerializer, AttachmentTagSerializer, AttachmentAccessLogSerializer
from django.utils import timezone
# ViewSet for AttachmentTag
from rest_framework import permissions
class AttachmentTagViewSet(viewsets.ModelViewSet):
    queryset = AttachmentTag.objects.all()
    serializer_class = AttachmentTagSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet for AttachmentAccessLog (read-only)
class AttachmentAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttachmentAccessLog.objects.all()
    serializer_class = AttachmentAccessLogSerializer
    permission_classes = [permissions.IsAdminUser]


# ViewSet for AttachmentComment
from rest_framework import permissions
class AttachmentCommentViewSet(viewsets.ModelViewSet):
    queryset = AttachmentComment.objects.all()
    serializer_class = AttachmentCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttachmentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Attachment model stores uploader in `uploaded_by`.
        serializer.save(uploaded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Only show attachments that are approved or owned/shared/non-confidential.
        # Previously we applied `is_approved=True` first which excluded
        # attachments uploaded by the current user (which are often unapproved
        # immediately after upload) and caused detail actions to return 404.
        now = timezone.now()
        qs = qs.exclude(
            expiry_date__isnull=False,
            expiry_date__lt=now
        ).filter(
            models.Q(is_approved=True) |
            models.Q(shared_with_users=user) |
            models.Q(shared_with_groups__in=user.groups.all()) |
            models.Q(uploaded_by=user) |
            models.Q(is_confidential=False)
        ).distinct()
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Enforce download limit
        if instance.download_limit is not None and instance.download_count >= instance.download_limit:
            return Response({'detail': 'Download limit reached.'}, status=403)
        # Log access
        AttachmentAccessLog.objects.create(attachment=instance, user=request.user, action='view')
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        instance = self.get_object()
        if instance.download_limit is not None and instance.download_count >= instance.download_limit:
            return Response({'detail': 'Download limit reached.'}, status=403)
        instance.download_count += 1
        instance.save()
        AttachmentAccessLog.objects.create(attachment=instance, user=request.user, action='download')
        # Implement file response logic as needed
        return Response({'status': 'downloaded', 'download_count': instance.download_count})

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response({'status': 'soft_deleted'})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = True
        obj.save()
        return Response({'status': 'restored'})

    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        obj = self.get_object()
        obj.download_count += 1
        obj.save()
        return Response({'download_count': obj.download_count})

