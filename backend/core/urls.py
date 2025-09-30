from django.urls import path
urlpatterns = []
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Uzuri University API",
        default_version='v1',
        description="API documentation for Uzuri University",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, CustomUserViewSet, StudentProfileViewSet, RegisterView, UserDetailView,
    ProgramViewSet, CourseViewSet, UnitViewSet, RegistrationViewSet, TranscriptViewSet, GradeViewSet,
    AssignmentViewSet, SubmissionViewSet, InvoiceViewSet, TransactionViewSet, ReceiptViewSet, ScholarshipViewSet,
    HostelApplicationViewSet, LeaveRequestViewSet, NotificationViewSet, MessageViewSet, TicketViewSet,
    AuditLogViewSet, AdminActionLogViewSet, SystemMetricViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', StudentProfileViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'units', UnitViewSet)
router.register(r'registrations', RegistrationViewSet)
router.register(r'transcripts', TranscriptViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'receipts', ReceiptViewSet)
router.register(r'scholarships', ScholarshipViewSet)
router.register(r'hostel-applications', HostelApplicationViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'admin-action-logs', AdminActionLogViewSet)
router.register(r'system-metrics', SystemMetricViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('provisional-results/', include('provisional_results.urls')),
    path('final-results/', include('final_results.urls')),
    path('docs/', include('core.urls_swagger')),
    path('lecturer-evaluation/', include('lecturer_evaluation.urls')),
    path('disciplinary/', include('disciplinary.urls')),
    path('academic-leave/', include('academic_leave.urls')),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', UserDetailView.as_view(), name='auth-me'),
    path('auth/', include('allauth.urls')),
        path('', include('core.urls_dashboard')),
        path('', include('core.urls_reporting')),
        path('', include('core.urls_notifications')),
        path('', include('core.urls_ai')),
        path('', include('core.urls_integration')),
        path('', include('core.urls_mobile')),
    ]
