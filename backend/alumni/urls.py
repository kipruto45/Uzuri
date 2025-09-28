from rest_framework.routers import DefaultRouter
from .views import AlumniProfileViewSet, JobPostingViewSet

router = DefaultRouter()
router.register(r'alumni-profiles', AlumniProfileViewSet)
router.register(r'job-postings', JobPostingViewSet)

urlpatterns = router.urls
