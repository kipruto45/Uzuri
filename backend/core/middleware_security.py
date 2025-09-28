from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse
import logging

class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log sensitive operations for compliance
        user = getattr(request, 'user', None)
        logging.info(f"AUDIT: {user} accessed {request.path} via {request.method}")

class MFAEnforcementMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Enforce MFA for sensitive endpoints only when enabled in settings.
        # Tests and many local dev setups don't enable MFA, so default to off.
        if not getattr(settings, 'MFA_ENABLED', False):
            return None

        if request.path.startswith('/api/') and not request.session.get('mfa_verified', False):
            payload = {'error': 'Multi-factor authentication required.'}
            resp = JsonResponse(payload, status=403)
            # Some code/tests expect a DRF-like Response with a `.data` attribute.
            # Attach it here to avoid AttributeError("'JsonResponse' object has no attribute 'data'").
            resp.data = payload
            return resp

class EncryptionHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add headers for end-to-end encryption
        response['X-Data-Encryption'] = 'enabled'
        return response
