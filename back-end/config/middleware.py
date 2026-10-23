from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import patch_vary_headers
from urllib.parse import urlsplit


class FrontendCorsMiddleware:
    """Allow the separately served frontend to call the JSON chat API."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get('Origin')
        allowed = request.path.startswith('/chat/') and (
            origin in settings.FRONTEND_ORIGINS or self._same_host_frontend(request, origin)
        )

        if allowed and request.method == 'OPTIONS':
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        if allowed:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            patch_vary_headers(response, ['Origin'])

        if request.path.startswith('/chat/'):
            response['Cache-Control'] = 'no-store'

        return response

    @staticmethod
    def _same_host_frontend(request, origin):
        if not settings.DEBUG or not origin:
            return False

        try:
            frontend = urlsplit(origin)
            api_host = urlsplit(f'http://{request.get_host()}').hostname
            return (
                frontend.scheme == 'http'
                and frontend.port == 5500
                and frontend.hostname == api_host
                and not frontend.path
                and not frontend.query
                and not frontend.fragment
                and not frontend.username
            )
        except ValueError:
            return False
