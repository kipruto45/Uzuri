from rest_framework.routers import DefaultRouter
from .views import LearningPathwayViewSet, MicroCredentialViewSet

router = DefaultRouter()
router.register(r'learning-pathways', LearningPathwayViewSet)
router.register(r'micro-credentials', MicroCredentialViewSet)

urlpatterns = router.urls
