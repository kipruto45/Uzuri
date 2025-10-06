from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UnitRegistrationViewSet, available_units, add_unit, drop_unit, unit_dashboard, bulk_approve_registrations, registration_report, UnitOfferingViewSet, registration_history, download_receipt, registration_stats, export_registrations_csv, bulk_drop_units, bulk_add_units

router = DefaultRouter()
router.register(r'unit/registrations', UnitRegistrationViewSet, basename='unit-registration')
router.register(r'unit/offerings', UnitOfferingViewSet, basename='unit-offering')

urlpatterns = router.urls + [
    path('unit/available/', available_units, name='unit-available'),
    path('unit/add/', add_unit, name='unit-add'),
    path('unit/drop/', drop_unit, name='unit-drop'),
    path('unit/dashboard/', unit_dashboard, name='unit-dashboard'),
    path('unit/bulk-approve/', bulk_approve_registrations, name='unit-bulk-approve'),
    path('unit/report/', registration_report, name='unit-report'),
    path('unit/history/', registration_history, name='unit-history'),
    path('unit/receipt/<int:reg_id>/', download_receipt, name='unit-receipt'),
    path('unit/stats/', registration_stats, name='unit-stats'),
    path('unit/export/', export_registrations_csv, name='unit-export'),
    path('unit/bulk-drop/', bulk_drop_units, name='unit-bulk-drop'),
    path('unit/bulk-add/', bulk_add_units, name='unit-bulk-add'),
]
