
from rest_framework import serializers
from .models import AttachmentTag, AttachmentAccessLog, Attachment, AttachmentNotificationLog, AttachmentComment
# Serializer for AttachmentTag
class AttachmentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentTag
        fields = ["id", "name"]

# Serializer for AttachmentAccessLog
class AttachmentAccessLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = AttachmentAccessLog
        fields = ["id", "attachment", "user", "action", "timestamp"]

# Serializer for AttachmentComment
class AttachmentCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AttachmentComment
        fields = ["id", "attachment", "user", "comment", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
from rest_framework import serializers

class AttachmentSerializer(serializers.ModelSerializer):
    tags = AttachmentTagSerializer(many=True, read_only=True)
    shared_with_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    shared_with_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    file_preview = serializers.FileField(read_only=True)

    class Meta:
        model = Attachment
        fields = '__all__'

