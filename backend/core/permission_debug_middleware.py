import logging
import traceback
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

class PermissionDebugMiddleware:
    """Test-only middleware to log stack traces when PermissionDenied is raised
    or when a response with status_code==403 is returned. This file is added
    temporarily to help diagnose why tests hit 403 responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except PermissionDenied:
            logger.error('PermissionDenied raised for %s %s', request.method, request.path, exc_info=True)
            # Re-raise so test runner continues to show failure behavior
            raise
        # If a downstream component returned a 403 response (without raising), log stack
        try:
            status_code = getattr(response, 'status_code', None)
            if status_code == 403:
                # Log response introspection to help pinpoint origin
                try:
                    cls = response.__class__
                    content = getattr(response, 'content', None)
                    # headers access: response._headers for older Django, or response.items()
                    headers = None
                    try:
                        headers = dict(response.items())
                    except Exception:
                        headers = getattr(response, '__dict__', {})
                    logger.error('Response with 403 returned for %s %s; class=%s, headers=%s, content=%s', request.method, request.path, cls, headers, content)
                except Exception:
                    logger.exception('Failed to introspect 403 response')
                logger.error('Current stack:\n%s', ''.join(traceback.format_stack()))
        except Exception:
            logger.exception('Error while inspecting response for 403')
        return response
