from django.urls import path
from .views_dashboard import (
    StudentDashboardView,
    LecturerDashboardView,
    RegistrarDashboardView,
    FinanceDashboardView,
    HODDashboardView,
    ITAdminDashboardView,
    UnifiedDashboardView,
)

urlpatterns = [
    path('student/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('lecturer/', LecturerDashboardView.as_view(), name='lecturer-dashboard'),
    path('registrar/', RegistrarDashboardView.as_view(), name='registrar-dashboard'),
    path('finance/', FinanceDashboardView.as_view(), name='finance-dashboard'),
    path('hod/', HODDashboardView.as_view(), name='hod-dashboard'),
    path('it/', ITAdminDashboardView.as_view(), name='it-dashboard'),
    path('unified/', UnifiedDashboardView.as_view(), name='unified-dashboard'),
]
