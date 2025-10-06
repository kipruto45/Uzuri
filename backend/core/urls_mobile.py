from django.urls import path
from .views_mobile import OfflineCacheManifestView

urlpatterns = [
    path('api/mobile/offline-manifest/', OfflineCacheManifestView.as_view(), name='offline-manifest'),
]
