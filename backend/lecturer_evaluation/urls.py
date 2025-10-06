from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentEvaluationViewSet, EvaluationSummaryViewSet

router = DefaultRouter()
router.register(r'student-evaluations', StudentEvaluationViewSet, basename='student-evaluations')
router.register(r'evaluation-summary', EvaluationSummaryViewSet, basename='evaluation-summary')

urlpatterns = [
    path('', include(router.urls)),
]
