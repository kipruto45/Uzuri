from rest_framework.routers import DefaultRouter
from .views import ProctoringSessionViewSet, PlagiarismReportViewSet

router = DefaultRouter()
router.register(r'proctoring-sessions', ProctoringSessionViewSet)
router.register(r'plagiarism-reports', PlagiarismReportViewSet)

urlpatterns = router.urls
