
from django.urls import path
from .views import (
    StudentProfileViewSet,
    IDCardReplacementRequestAdminViewSet,
    StudentProfileAPIView,
    IDCardRequestAPIView,
    IDCardDownloadAPIView,
)

urlpatterns = [
    # Explicit mappings so tests that hit '/api/student/profile/' operate against the
    # viewset actions we expect (GET -> get_profile, PATCH -> update_profile).
    # APIView-backed explicit mappings used by tests (avoid router redirects)
    path('api/student/profile/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('api/student/profile/id-card/request/', IDCardRequestAPIView.as_view(), name='student-profile-id-card-request-explicit'),
    path('api/student/profile/id-card/', IDCardDownloadAPIView.as_view(), name='student-profile-id-card'),
]
