from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DisciplinaryCaseViewSet, EvidenceViewSet, HearingViewSet,
    DisciplinaryActionViewSet, AppealViewSet, AuditTrailViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'cases', DisciplinaryCaseViewSet, basename='disciplinary-cases')
router.register(r'evidence', EvidenceViewSet, basename='disciplinary-evidence')
router.register(r'hearings', HearingViewSet, basename='disciplinary-hearings')
router.register(r'actions', DisciplinaryActionViewSet, basename='disciplinary-actions')
router.register(r'appeals', AppealViewSet, basename='disciplinary-appeals')
router.register(r'audit', AuditTrailViewSet, basename='disciplinary-audit')
router.register(r'notifications', NotificationViewSet, basename='disciplinary-notifications')

urlpatterns = [
    path('', include(router.urls)),
]
