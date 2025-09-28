from rest_framework.routers import DefaultRouter
from .views import MarketplaceItemViewSet, PurchaseViewSet

router = DefaultRouter()
router.register(r'items', MarketplaceItemViewSet)
router.register(r'purchases', PurchaseViewSet)

urlpatterns = router.urls
