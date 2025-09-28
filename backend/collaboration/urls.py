from rest_framework.routers import DefaultRouter
from .views import CollaborationSessionViewSet, DocumentEditViewSet, WhiteboardViewSet

router = DefaultRouter()
router.register(r'collaboration-sessions', CollaborationSessionViewSet)
router.register(r'document-edits', DocumentEditViewSet)
router.register(r'whiteboards', WhiteboardViewSet)

urlpatterns = router.urls
