from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, TransactionViewSet, ReceiptViewSet, FeeStructureViewSet, ScholarshipViewSet, AuditTrailViewSet
from .integration import MpesaWebhookView



router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'receipts', ReceiptViewSet, basename='receipt')
router.register(r'feestructure', FeeStructureViewSet, basename='feestructure')
router.register(r'scholarships', ScholarshipViewSet, basename='scholarship')
router.register(r'audittrails', AuditTrailViewSet, basename='audittrail')

urlpatterns = [
    path('api/fees/', include(router.urls)),
    path('api/fees/mpesa-webhook/', MpesaWebhookView.as_view(), name='mpesa-webhook'),
]
