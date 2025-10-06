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

# Frontend-friendly thin wrappers (so frontend can call /api/disciplinary/ and related endpoints)
case_list_create = DisciplinaryCaseViewSet.as_view({'get': 'list', 'post': 'create'})
case_analytics = DisciplinaryCaseViewSet.as_view({'get': 'analytics'})
case_add_evidence = DisciplinaryCaseViewSet.as_view({'post': 'add_evidence'})
case_submit_appeal = DisciplinaryCaseViewSet.as_view({'post': 'submit_appeal'})

urlpatterns = [
    path('', case_list_create, name='disciplinary-root'),
    path('analytics/', case_analytics, name='disciplinary-analytics'),
    path('<int:pk>/evidence/', case_add_evidence, name='disciplinary-add-evidence'),
    path('<int:pk>/appeal/', case_submit_appeal, name='disciplinary-submit-appeal'),
    # keep full router for admin/other programmatic access
    path('', include(router.urls)),
]
