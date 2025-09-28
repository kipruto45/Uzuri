from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls
