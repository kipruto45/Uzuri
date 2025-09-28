from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, DisciplinaryActionViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet)
router.register(r'disciplinary-actions', DisciplinaryActionViewSet)

urlpatterns = router.urls
