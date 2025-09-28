from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include
from .views import BadgeViewSet, AwardedBadgeViewSet, AIInsightLogViewSet, InsightsViewSet
from .views import (
    GroupViewSet, GroupAssignmentViewSet, PeerReviewViewSet, LiveSessionViewSet,
    GuardianViewSet, StudentGuardianLinkViewSet, AuditLogViewSet,
    MarketplaceItemViewSet, PurchaseViewSet, DashboardWidgetViewSet
)
from .views import LoginWithEmailView

router = DefaultRouter()
# Routers for main resources (add more as needed)
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'materials', LearningMaterialViewSet, basename='material')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', AssignmentSubmissionViewSet, basename='submission')
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'attempts', QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'forums', ForumThreadViewSet, basename='forum-thread')
router.register(r'replies', ForumReplyViewSet, basename='forum-reply')
router.register(r'progress', ProgressTrackerViewSet, basename='progress')
router.register(r'notifications', EmasomoNotificationViewSet, basename='emasomo-notification')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'awarded-badges', AwardedBadgeViewSet, basename='awardedbadge')
router.register(r'ai-insights', AIInsightLogViewSet, basename='aiinsightlog')
router.register(r'insights', InsightsViewSet, basename='insights')
router.register(r'groups', GroupViewSet)
router.register(r'group-assignments', GroupAssignmentViewSet)
router.register(r'peer-reviews', PeerReviewViewSet)
router.register(r'live-sessions', LiveSessionViewSet)
router.register(r'guardians', GuardianViewSet)
router.register(r'student-guardian-links', StudentGuardianLinkViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'marketplace-items', MarketplaceItemViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'dashboard-widgets', DashboardWidgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login-with-email/', LoginWithEmailView.as_view(), name='login-with-email'),
]
