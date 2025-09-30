"""No-op debug middleware module.

This file previously contained temporary test-only debugging middleware.
It has been replaced with a small no-op placeholder to avoid leaving
test-only logic in the runtime path. Remove this file entirely if you
prefer.

The middleware below is intentionally minimal so importing this module
never raises and code that references the callable keeps working.
"""

from typing import Callable


def noop_middleware(get_response: Callable):
    """Return a middleware that simply calls the next layer.

    Keep this around as a placeholder so imports don't break if the
    temporary debug middleware was referenced in settings.
    """

    def middleware(request):
        return get_response(request)

    return middleware
