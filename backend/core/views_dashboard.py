from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, Q, Sum
from core.models_shared import CustomUser, StudentProfile
from notifications.models import Notification
from fees.models import Invoice, Transaction
 # from academic_leave.models import AcademicLeave
from unit_registration.models import UnitRegistration
from graduation.models import GraduationApplication
from timetable.models import Timetable
from calendar_app.models import Event
 # from core.ai import get_course_recommendations, predict_performance, detect_threats
 # from core.blockchain import get_blockchain_records, record_transaction
 # from core.accessibility import get_accessibility_features
 # from core.mobile import get_mobile_manifest
 # from core.integrations import get_lms_data, get_payment_gateway_status, get_cloud_storage_links
 # from core.tasks import send_notification_task, run_approval_workflow
from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.utils import get_unread_count, get_notification_types, get_delivery_status

class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        profile = StudentProfile.objects.filter(user=user).first()
        units = UnitRegistration.objects.filter(student=user)
        invoices = Invoice.objects.filter(student=user)
        transactions = Transaction.objects.filter(student=user)
        results = profile.results.all() if profile else []
        leaves = AcademicLeave.objects.filter(student=user)
        graduation = GraduationApplication.objects.filter(student=user).first()
        timetable = Timetable.objects.filter(student=user)
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_count = get_unread_count(user)
        notification_types = get_notification_types(user)
        delivery_status = get_delivery_status(user)
        data = {
            "profile": profile,
            "units": units,
            "invoices": invoices,
            "transactions": transactions,
            "results": results,
            "leaves": leaves,
            "graduation": graduation,
            "timetable": timetable,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
        }
        return Response(data)

class LecturerDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        classes = Timetable.objects.filter(lecturer=user)
        grades = user.lecturer_grades.all() if hasattr(user, 'lecturer_grades') else []
        attendance = user.lecturer_attendance.all() if hasattr(user, 'lecturer_attendance') else []
        materials = user.lecturer_materials.all() if hasattr(user, 'lecturer_materials') else []
        reports = user.lecturer_reports.all() if hasattr(user, 'lecturer_reports') else []
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_count = get_unread_count(user)
        notification_types = get_notification_types(user)
        delivery_status = get_delivery_status(user)
        data = {
            "classes": classes,
            "grades": grades,
            "attendance": attendance,
            "materials": materials,
            "reports": reports,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
        }
        return Response(data)

class RegistrarDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        students = StudentProfile.objects.all()
        registrations = UnitRegistration.objects.filter(status='pending')
        exam_cards = GraduationApplication.objects.filter(status='pending')
        transcripts = [s.get_transcript() for s in students]
        status_changes = [] # Placeholder for status changes
        calendar = Event.objects.filter(Q(target_roles__contains='registrar') | Q(target_users=request.user))
        compliance_reports = [] # Placeholder
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = get_unread_count(request.user)
        notification_types = get_notification_types(request.user)
        delivery_status = get_delivery_status(request.user)
        analytics = {
            "registration_workflow": run_approval_workflow(),
            "compliance": {}, # Placeholder
        }
        accessibility_features = get_accessibility_features(request.user)
        data = {
            "students": students,
            "registrations": registrations,
            "exam_cards": exam_cards,
            "transcripts": transcripts,
            "status_changes": status_changes,
            "calendar": calendar,
            "compliance_reports": compliance_reports,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
            "analytics": analytics,
            "accessibility_features": accessibility_features,
        }
        return Response(data)

class FinanceDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payments = Transaction.objects.all()
        statements = Invoice.objects.all()
        scholarships = [] # Placeholder for scholarship aggregation
        clearance = [] # Placeholder for financial clearance
        overdue = Transaction.objects.filter(status='overdue')
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = get_unread_count(request.user)
        notification_types = get_notification_types(request.user)
        delivery_status = get_delivery_status(request.user)
        analytics = {
            "cash_flow": payments.aggregate(total=Sum('amount')),
            "pending_payments": overdue.count(),
            "forecasting": {}, # Placeholder
        }
    # blockchain_financial_records = get_blockchain_records(request.user)
    # payment_gateway_status = get_payment_gateway_status()
    # accessibility_features = get_accessibility_features(request.user)
        data = {
            "payments": payments,
            "statements": statements,
            "scholarships": scholarships,
            "clearance": clearance,
            "overdue": overdue,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
            "analytics": analytics,
            # "blockchain_financial_records": blockchain_financial_records,
            # "payment_gateway_status": payment_gateway_status,
            # "accessibility_features": accessibility_features,
        }
        return Response(data)

class HODDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        department_students = StudentProfile.objects.filter(department=request.user.department)
        approvals = UnitRegistration.objects.filter(department=request.user.department, status='pending')
        reports = [s.get_department_report() for s in department_students]
        schedules = Timetable.objects.filter(department=request.user.department)
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = get_unread_count(request.user)
        notification_types = get_notification_types(request.user)
        delivery_status = get_delivery_status(request.user)
        analytics = {
            "department_kpis": {}, # Placeholder
            # "workflow_approvals": run_approval_workflow(),
        }
    # accessibility_features = get_accessibility_features(request.user)
        data = {
            "department_students": department_students,
            "approvals": approvals,
            "reports": reports,
            "schedules": schedules,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
            "analytics": analytics,
            # "accessibility_features": accessibility_features,
        }
        return Response(data)

class ITAdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_activity = []  # Placeholder for user activity
        backup_status = {}  # Placeholder for backup status
        data = {
            "user_activity": user_activity,
            "backup_status": backup_status,
        }
        return Response(data)

class UnifiedDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        role_dashboards = {
            "student": StudentDashboardView().get(request).data,
            "lecturer": LecturerDashboardView().get(request).data,
            "registrar": RegistrarDashboardView().get(request).data,
            "finance": FinanceDashboardView().get(request).data,
            "hod": HODDashboardView().get(request).data,
            "it_admin": ITAdminDashboardView().get(request).data,
        }
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = get_unread_count(request.user)
        notification_types = get_notification_types(request.user)
        delivery_status = get_delivery_status(request.user)
        analytics = {} # Placeholder for unified analytics
    # mobile_manifest = get_mobile_manifest(request.user)
    # accessibility_features = get_accessibility_features(request.user)
    # blockchain_records = get_blockchain_records(request.user)
        data = {
            "role_dashboards": role_dashboards,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
            "analytics": analytics,
            # "mobile_manifest": mobile_manifest,
            # "accessibility_features": accessibility_features,
            # "blockchain_records": blockchain_records,
        }
        return Response(data)

# Workflow automation: signals for approval and notification
## Workflow automation: signals for approval and notification (commented out, missing functions)
# @receiver(post_save, sender=UnitRegistration)
# def unit_registration_approval_workflow(sender, instance, created, **kwargs):
#     if created and instance.status == 'pending':
#         run_approval_workflow(instance)
#         send_notification_task(instance.student.user, 'Unit registration pending approval.')
#
# @receiver(post_save, sender=GraduationApplication)
# def graduation_approval_workflow(sender, instance, created, **kwargs):
#     if created and instance.status == 'pending':
#         run_approval_workflow(instance)
#         send_notification_task(instance.student.user, 'Graduation application pending approval.')
