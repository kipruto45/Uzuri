# Make this script runnable directly: configure Django and set up the ORM
import os
import sys
import traceback
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzuri_university.settings')
import django
django.setup()
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

print('Starting public_analytics reproduction')
rf = RequestFactory()
request = rf.get('/api/notifications/analytics/')
# Many middleware set attributes on request; ensure session exists if code expects it.
# RequestFactory by default doesn't provide a session; attach a simple dict-like session stub.
class SimpleSession(dict):
    def get(self, k, default=None):
        return super().get(k, default)

request.session = SimpleSession()
request.user = AnonymousUser()

try:
    from notifications.views import public_analytics
    resp = public_analytics(request)
    # If DRF Response, it may not be rendered yet; try to access resp.status_code and resp.data
    status = getattr(resp, 'status_code', None)
    data = getattr(resp, 'data', None)
    print('Response status:', status)
    print('Response data:', data)
except Exception:
    print('Exception during public_analytics call:')
    traceback.print_exc()
