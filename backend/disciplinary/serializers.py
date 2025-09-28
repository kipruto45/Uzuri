from rest_framework import serializers
from .models import DisciplinaryCase, Evidence, Hearing, DisciplinaryAction, Appeal, AuditTrail, DisciplinaryNotification

class DisciplinaryCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryCase
        fields = '__all__'

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = '__all__'

class HearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hearing
        fields = '__all__'

class DisciplinaryActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryAction
        fields = '__all__'

class AppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = '__all__'

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryNotification
        fields = '__all__'
