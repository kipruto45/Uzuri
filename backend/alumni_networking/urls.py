from rest_framework.routers import DefaultRouter
from .views import AlumniMentorViewSet, MentorshipMatchViewSet

router = DefaultRouter()
router.register(r'alumni-mentors', AlumniMentorViewSet)
router.register(r'mentorship-matches', MentorshipMatchViewSet)

urlpatterns = router.urls
