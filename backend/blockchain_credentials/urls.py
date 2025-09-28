from rest_framework.routers import DefaultRouter
from .views import BlockchainCredentialViewSet

router = DefaultRouter()
router.register(r'blockchain-credentials', BlockchainCredentialViewSet)

urlpatterns = router.urls
