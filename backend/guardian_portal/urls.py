from rest_framework.routers import DefaultRouter
from .views import GuardianViewSet, StudentGuardianLinkViewSet

router = DefaultRouter()
router.register(r'guardians', GuardianViewSet)
router.register(r'student-guardian-links', StudentGuardianLinkViewSet)

urlpatterns = router.urls
