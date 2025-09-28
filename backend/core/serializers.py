from rest_framework import serializers
from .models import CustomUser, Role, StudentProfile

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'student_number', 'first_name', 'last_name', 'role', 'is_active', 'photo']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'student_number', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            student_number=validated_data.get('student_number'),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    student_id = serializers.CharField(read_only=True)
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id', 'program', 'year', 'contact_info', 'emergency_contact', 'gpa', 'digital_id_qr']

# Academic
from .models import Program, Course, Unit, Registration, Transcript, Grade, Assignment, Submission
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

# Finance
from .models import Invoice, Transaction, Receipt, Scholarship
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'

# Hostel & Leave
from .models import HostelApplication, LeaveRequest
class HostelApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelApplication
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

# Notifications & Messaging
from .models import Notification, Message, Ticket
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

# Admin & System
from .models import AuditLog, AdminActionLog, SystemMetric
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class AdminActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActionLog
        fields = '__all__'

class SystemMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMetric
        fields = '__all__'

# New Student Features
from .models import ExamCard, LecturerEvaluation, DisciplinaryCase, FieldAttachment, Clearance, GraduationApplication, Timetable, EMasomoMaterial
class ExamCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCard
        fields = '__all__'

class LecturerEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerEvaluation
        fields = '__all__'

class DisciplinaryCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryCase
        fields = '__all__'

class FieldAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldAttachment
        fields = '__all__'

class ClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clearance
        fields = '__all__'

class GraduationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationApplication
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'

class EMasomoMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EMasomoMaterial
        fields = '__all__'
