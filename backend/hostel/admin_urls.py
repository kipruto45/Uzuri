from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminHostelViewSet

router = DefaultRouter()
router.register(r'admin/hostel', AdminHostelViewSet, basename='admin-hostel')

urlpatterns = router.urls
