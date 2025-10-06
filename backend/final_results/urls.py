from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinalResultViewSet

router = DefaultRouter()
router.register(r'results', FinalResultViewSet, basename='final-results')

urlpatterns = [
    path('', include(router.urls)),
]
