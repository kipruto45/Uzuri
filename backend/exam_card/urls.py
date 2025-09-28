from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ExamCardViewSet, exam_card_types, digital_verify

router = DefaultRouter()
router.register(r'exam/cards', ExamCardViewSet, basename='exam-card')

urlpatterns = router.urls + [
    path('exam/types/', exam_card_types, name='exam-card-types'),
    path('exam/digital-verify/', digital_verify, name='exam-card-digital-verify'),
]
