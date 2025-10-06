from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClearanceDepartmentViewSet, ClearanceRequestViewSet, ClearanceApprovalViewSet, ClearanceDocumentViewSet,
    ClearanceWorkflowLogViewSet, ClearanceNotificationViewSet, ClearanceCommentViewSet, ClearanceDigitalSignatureViewSet, ClearanceAuditTrailViewSet
)

router = DefaultRouter()
router.register(r'departments', ClearanceDepartmentViewSet)
router.register(r'requests', ClearanceRequestViewSet)
router.register(r'approvals', ClearanceApprovalViewSet)
router.register(r'documents', ClearanceDocumentViewSet)
router.register(r'workflow-logs', ClearanceWorkflowLogViewSet)
router.register(r'notifications', ClearanceNotificationViewSet)
router.register(r'comments', ClearanceCommentViewSet)
router.register(r'digital-signatures', ClearanceDigitalSignatureViewSet)
router.register(r'audit-trails', ClearanceAuditTrailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
