from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AcademicLeaveRequestViewSet, AcademicLeaveApprovalViewSet,
    AcademicLeaveDocumentViewSet, AcademicLeaveAuditViewSet
)

router = DefaultRouter()
router.register(r'requests', AcademicLeaveRequestViewSet, basename='academic-leave-requests')
router.register(r'approval', AcademicLeaveApprovalViewSet, basename='academic-leave-approval')
router.register(r'documents', AcademicLeaveDocumentViewSet, basename='academic-leave-documents')
router.register(r'audit', AcademicLeaveAuditViewSet, basename='academic-leave-audit')

urlpatterns = [
    path('', include(router.urls)),
]
