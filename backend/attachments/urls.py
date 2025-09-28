from rest_framework.routers import DefaultRouter
from .views import AttachmentViewSet, AttachmentCommentViewSet, AttachmentTagViewSet, AttachmentAccessLogViewSet


router = DefaultRouter()
router.register(r'attachments', AttachmentViewSet)
router.register(r'comments', AttachmentCommentViewSet)
router.register(r'tags', AttachmentTagViewSet)
router.register(r'access-logs', AttachmentAccessLogViewSet)

urlpatterns = router.urls
