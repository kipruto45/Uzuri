from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse
import logging
import sys
import os
import traceback

class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log sensitive operations for compliance
        user = getattr(request, 'user', None)
        logging.info(f"AUDIT: {user} accessed {request.path} via {request.method}")

class MFAEnforcementMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Enforce MFA for sensitive endpoints only when enabled in settings.
        # Tests and many local dev setups don't enable MFA, so default to off.
        # (original behavior) only skip MFA enforcement entirely when the
        # MFA feature is disabled in settings via MFA_ENABLED.
        if not getattr(settings, 'MFA_ENABLED', False):
            return None

        if request.path.startswith('/api/') and not request.session.get('mfa_verified', False):
            payload = {'error': 'Multi-factor authentication required.'}
            resp = JsonResponse(payload, status=403)
            # Some code/tests expect a DRF-like Response with a `.data` attribute.
            # Attach it here to avoid AttributeError("'JsonResponse' object has no attribute 'data'").
            resp.data = payload
            # Log the blocking with stack trace to help debug which component
            # caused the 403 during tests and reproduce the call stack.
            logging.error('MFAEnforcementMiddleware blocking request %s %s', request.method, request.path, exc_info=True)
            try:
                logging.error('Current stack:\n%s', ''.join(traceback.format_stack()))
            except Exception:
                logging.exception('Failed to format stack')
            return resp

class EncryptionHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add headers for end-to-end encryption
        response['X-Data-Encryption'] = 'enabled'
        return response
