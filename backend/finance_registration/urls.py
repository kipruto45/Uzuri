from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import FinanceCategoryViewSet, FinanceRegistrationViewSet, FinanceInvoiceViewSet, finance_dashboard


from .views import finance_dashboard

router = DefaultRouter()
router.register(r'finance/categories', FinanceCategoryViewSet, basename='finance-category')
router.register(r'finance/registrations', FinanceRegistrationViewSet, basename='finance-registration')
router.register(r'finance/invoices', FinanceInvoiceViewSet, basename='finance-invoice')

urlpatterns = router.urls + [
	# Student dashboard API
	path('finance/dashboard/', finance_dashboard, name='finance-dashboard'),
]
