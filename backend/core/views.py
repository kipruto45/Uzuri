from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# Admin broadcast urgent alerts endpoint
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def broadcast_urgent_alert(request):
    message = request.data.get('message')
    if not message:
        return Response({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)
    from notifications.models import Notification
    from .models import CustomUser
    students = CustomUser.objects.filter(is_active=True, is_staff=False)
    for student in students:
        Notification.objects.create(
            user=student,
            message=message,
            type="emergency_alert",
        )
    return Response({'detail': 'Alert broadcasted to all students.'}, status=status.HTTP_200_OK)
# Academic module endpoints
from .serializers import ProgramSerializer, CourseSerializer, UnitSerializer
from .permissions import IsStudent, IsLecturer, IsFinanceStaff, IsRegistrar, IsSystemAdmin, IsParentGuardian, IsGuest, IsSupportStaff
from .models import Program, Course, Unit
from rest_framework import viewsets, permissions
class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsStudent]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAdminUser]
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import CustomUser, Role, StudentProfile, Program, Course, Unit, Registration, Transcript, Grade, Assignment, Submission, Invoice, Transaction, Receipt, Scholarship, HostelApplication, LeaveRequest, Notification, Message, Ticket, AuditLog, AdminActionLog, SystemMetric
from .serializers import CustomUserSerializer, RoleSerializer, StudentProfileSerializer, RegisterSerializer
from .permissions import IsStudent, IsLecturer, IsFinanceStaff, IsRegistrar, IsSystemAdmin, IsParentGuardian, IsGuest, IsSupportStaff
from .business_logic import register_unit, pay_invoice, has_role
from django.contrib.auth import get_user_model
from .models import (
    ExamCard, LecturerEvaluation, DisciplinaryCase, FieldAttachment, Clearance, GraduationApplication, Timetable, EMasomoMaterial
)
from .serializers import (
    ExamCardSerializer, LecturerEvaluationSerializer, DisciplinaryCaseSerializer, FieldAttachmentSerializer, ClearanceSerializer, GraduationApplicationSerializer, TimetableSerializer, EMasomoMaterialSerializer
)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSystemAdmin]

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsStudent]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        # Only allow students to view/edit their own profile
        return StudentProfile.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Only allow editing own profile
        instance = self.get_object()
        if instance.user != request.user:
            return Response({
                'error': 'Permission denied.',
                'detail': 'You can only update your own profile.'
            }, status=403)
        return super().update(request, *args, **kwargs)

# Student module endpoints
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        student_profile = getattr(request.user, 'studentprofile', None)
        unit_id = request.data.get('unit')
        if not unit_id:
            return Response({'error': 'Unit ID is required.'}, status=400)
        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found.', 'detail': f'No unit with id {unit_id}.'}, status=404)
        if not student_profile:
            return Response({'error': 'Student profile not found.'}, status=404)
        success, message = register_unit(student_profile, unit)
        if success:
            return Response({'message': message}, status=201)
        else:
            return Response({'error': message, 'detail': 'Registration failed. Please check prerequisites or contact admin.'}, status=400)

class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    permission_classes = [IsStudent]

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    permission_classes = [IsLecturer]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    permission_classes = [IsLecturer]

# Admin module endpoints
class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    permission_classes = [IsSystemAdmin]

class AdminActionLogViewSet(viewsets.ModelViewSet):
    queryset = AdminActionLog.objects.all()
    permission_classes = [IsSystemAdmin]

# Registrar module endpoints
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsRegistrar]

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    permission_classes = [IsRegistrar]

# Finance module endpoints
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    permission_classes = [IsFinanceStaff]

    def pay(self, request, pk=None):
        invoice = self.get_object()
        student_profile = invoice.student
        amount = request.data.get('amount')
        method = request.data.get('method')
        reference = request.data.get('reference')
        if not amount or not method or not reference:
            return Response({'error': 'All payment fields are required.'}, status=400)
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return Response({'error': 'Amount must be a valid number.'}, status=400)
        success, message = pay_invoice(student_profile, invoice, amount, method, reference)
        if success:
            return Response({'message': message}, status=200)
        else:
            return Response({'error': message, 'detail': 'Payment failed. Please check your details or contact support.'}, status=400)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsFinanceStaff]

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    permission_classes = [IsFinanceStaff]

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    permission_classes = [IsFinanceStaff]

# Lecturer module endpoints
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    permission_classes = [IsLecturer]

# Hostel & Leave
class HostelApplicationViewSet(viewsets.ModelViewSet):
    queryset = HostelApplication.objects.all()
    permission_classes = [IsStudent]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    permission_classes = [IsStudent]

# Notifications & Messaging
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    permission_classes = [IsSystemAdmin, IsFinanceStaff, IsRegistrar, IsLecturer, IsStudent, IsParentGuardian, IsSupportStaff]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsSystemAdmin, IsFinanceStaff, IsRegistrar, IsLecturer, IsStudent, IsParentGuardian, IsSupportStaff]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsSystemAdmin, IsFinanceStaff, IsRegistrar, IsLecturer, IsStudent, IsParentGuardian, IsSupportStaff]

# System metrics
class SystemMetricViewSet(viewsets.ModelViewSet):
    queryset = SystemMetric.objects.all()
    permission_classes = [IsSystemAdmin]

# Registration API
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# User detail API
class UserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

# JWT views are provided by simplejwt
# TokenObtainPairView: /api/auth/login/
# TokenRefreshView: /api/auth/refresh/

class ExamCardViewSet(viewsets.ModelViewSet):
    queryset = ExamCard.objects.all()
    serializer_class = ExamCardSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return ExamCard.objects.filter(student__user=self.request.user)

class LecturerEvaluationViewSet(viewsets.ModelViewSet):
    queryset = LecturerEvaluation.objects.all()
    serializer_class = LecturerEvaluationSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return LecturerEvaluation.objects.filter(student__user=self.request.user)

class DisciplinaryCaseViewSet(viewsets.ModelViewSet):
    queryset = DisciplinaryCase.objects.all()
    serializer_class = DisciplinaryCaseSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return DisciplinaryCase.objects.filter(student__user=self.request.user)

class FieldAttachmentViewSet(viewsets.ModelViewSet):
    queryset = FieldAttachment.objects.all()
    serializer_class = FieldAttachmentSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return FieldAttachment.objects.filter(student__user=self.request.user)

class ClearanceViewSet(viewsets.ModelViewSet):
    queryset = Clearance.objects.all()
    serializer_class = ClearanceSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return Clearance.objects.filter(student__user=self.request.user)

class GraduationApplicationViewSet(viewsets.ModelViewSet):
    queryset = GraduationApplication.objects.all()
    serializer_class = GraduationApplicationSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return GraduationApplication.objects.filter(student__user=self.request.user)

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return Timetable.objects.filter(student__user=self.request.user)

class EMasomoMaterialViewSet(viewsets.ModelViewSet):
    queryset = EMasomoMaterial.objects.all()
    serializer_class = EMasomoMaterialSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return EMasomoMaterial.objects.filter(unit__registration__student__user=self.request.user)
