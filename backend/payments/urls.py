from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentMethodViewSet, PaymentGatewayViewSet, PaymentViewSet, PaymentReceiptViewSet, PaymentAuditTrailViewSet, RefundViewSet,
    PaymentNotificationViewSet, PaymentReversalViewSet, PaymentDisputeViewSet, PaymentScheduleViewSet, PaymentIntegrationLogViewSet,
    PaymentCommentViewSet, PaymentAttachmentViewSet
)

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payment-gateways', PaymentGatewayViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'payment-receipts', PaymentReceiptViewSet)
router.register(r'payment-audit-trails', PaymentAuditTrailViewSet)
router.register(r'refunds', RefundViewSet)
router.register(r'payment-notifications', PaymentNotificationViewSet)
router.register(r'payment-reversals', PaymentReversalViewSet)
router.register(r'payment-disputes', PaymentDisputeViewSet)
router.register(r'payment-schedules', PaymentScheduleViewSet)
router.register(r'payment-integration-logs', PaymentIntegrationLogViewSet)
router.register(r'payment-comments', PaymentCommentViewSet)
router.register(r'payment-attachments', PaymentAttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
