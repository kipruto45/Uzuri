from django.urls import path
from .views_reporting import (
    AcademicReportView,
    FinancialReportView,
    DepartmentalReportView,
    ComplianceReportView,
    AnalyticsReportView,
)

urlpatterns = [
    path('api/report/academic/', AcademicReportView.as_view(), name='academic-report'),
    path('api/report/financial/', FinancialReportView.as_view(), name='financial-report'),
    path('api/report/departmental/', DepartmentalReportView.as_view(), name='departmental-report'),
    path('api/report/compliance/', ComplianceReportView.as_view(), name='compliance-report'),
    path('api/report/analytics/', AnalyticsReportView.as_view(), name='analytics-report'),
]
