from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentHostelViewSet

router = DefaultRouter()
router.register(r'student/hostel', StudentHostelViewSet, basename='student-hostel')

urlpatterns = router.urls
