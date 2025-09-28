from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, SurveyViewSet, SurveyResponseViewSet

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet)
router.register(r'surveys', SurveyViewSet)
router.register(r'survey-responses', SurveyResponseViewSet)

urlpatterns = router.urls
