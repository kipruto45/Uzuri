from django.urls import path
from .views_integration import (
    PaymentGatewayIntegrationView,
    LMSIntegrationView,
    CloudStorageIntegrationView,
    HRPayrollIntegrationView,
)

urlpatterns = [
    path('api/integration/payment-gateway/', PaymentGatewayIntegrationView.as_view(), name='integration-payment-gateway'),
    path('api/integration/lms/', LMSIntegrationView.as_view(), name='integration-lms'),
    path('api/integration/cloud-storage/', CloudStorageIntegrationView.as_view(), name='integration-cloud-storage'),
    path('api/integration/hr-payroll/', HRPayrollIntegrationView.as_view(), name='integration-hr-payroll'),
]
