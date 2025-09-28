from rest_framework.routers import DefaultRouter
from .views import ChatbotConversationViewSet, StudyRecommendationViewSet, AlertViewSet

router = DefaultRouter()
router.register(r'chatbot-conversations', ChatbotConversationViewSet)
router.register(r'study-recommendations', StudyRecommendationViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = router.urls
