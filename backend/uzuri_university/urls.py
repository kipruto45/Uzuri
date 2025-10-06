"""
URL configuration for uzuri_university project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include, re_path
# Project-level explicit analytics endpoint to avoid being shadowed by
# other routers that also register 'notifications' (core registers a
# notifications router at /api/). Put this before including core.urls so
# it takes precedence.
from notifications.views import public_analytics
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Uzuri University API",
        default_version='v1',
        description="API documentation for Uzuri University Management System",
        terms_of_service="https://www.uzuriuniversity.com/terms/",
        contact=openapi.Contact(email="support@uzuriuniversity.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Simple template-based pages for development / preview
    # development template routes are appended later — do not include here with an empty string
    path('api/notifications/analytics/', public_analytics),
    path('api/', include('core.urls')),
    path('api/attachments/', include('attachments.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/graduation/', include('graduation.urls')),
    path('api/clearance/', include('clearance.urls')),
    path('api/timetable/', include('timetable.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/emasomo/', include('emasomo.urls')),
    path('api/hostel/', include('hostel.urls')),
    path('api/calendar/', include('calendar_app.urls')),
    path('', include('my_profile.urls')),
    path('', include('fees.urls')),
    path('api/', include('unit_registration.urls')),
    path('api/', include('hostel.admin_urls')),
    path('api/', include('finance_registration.urls')),
    path('api/alumni-networking/', include('alumni_networking.urls')),
    path('api/personalization/', include('personalization.urls')),
    path('api/accessibility-ai/', include('accessibility_ai.urls')),
    path('api/compliance-audit/', include('compliance_audit.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Expose docs under /api/docs/ for frontend consumption
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    # Provide v1 compatibility endpoint - mirror existing api root
    path('api/v1/', include('core.urls')),
    path('api/v1/attachments/', include('attachments.urls')),
    path('api/v1/payments/', include('payments.urls')),
]
from .views_templates import dashboard, fees, hostel, academic_leave, attachments_index, notifications_index

# Development preview routes (simple HTML pages) -- not intended for production routing
urlpatterns += [
    path('', dashboard, name='dashboard_preview'),
    path('fees/', fees, name='fees_preview'),
    path('hostel/', hostel, name='hostel_preview'),
    path('academic_leave/', academic_leave, name='academic_leave_preview'),
    path('attachments/', attachments_index, name='attachments_preview'),
    path('notifications/', notifications_index, name='notifications_preview'),
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
