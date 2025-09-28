from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet

router = DefaultRouter()
router.register(r'workflows', WorkflowViewSet)

urlpatterns = router.urls
