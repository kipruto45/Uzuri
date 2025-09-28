
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginActivityViewSet, StudentProfileViewSet, IDCardReplacementRequestAdminViewSet, NotificationViewSet, AdminNotificationViewSet, StudentProfileAPIView, IDCardRequestAPIView


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginActivityViewSet, StudentProfileViewSet, IDCardReplacementRequestAdminViewSet, NotificationViewSet, AdminNotificationViewSet

router = DefaultRouter()
router.register(r'login-activity', LoginActivityViewSet, basename='login-activity')
router.register(r'student/profile', StudentProfileViewSet, basename='student-profile')
router.register(r'admin/id-card/requests', IDCardReplacementRequestAdminViewSet, basename='admin-id-card-requests')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'admin/notifications', AdminNotificationViewSet, basename='admin-notification')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/student/profile/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('api/student/profile/id-card/request/', IDCardRequestAPIView.as_view(), name='student-profile-id-card-request'),
]
