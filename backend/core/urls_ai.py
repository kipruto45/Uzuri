from django.urls import path
from .views_ai import (
    AcademicInsightsView,
    PerformancePredictionView,
    FinancialTrendsAIView,
    ThreatDetectionAIView,
)

urlpatterns = [
    path('api/ai/academic-insights/', AcademicInsightsView.as_view(), name='ai-academic-insights'),
    path('api/ai/performance-prediction/', PerformancePredictionView.as_view(), name='ai-performance-prediction'),
    path('api/ai/financial-trends/', FinancialTrendsAIView.as_view(), name='ai-financial-trends'),
    path('api/ai/threat-detection/', ThreatDetectionAIView.as_view(), name='ai-threat-detection'),
]
