from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response


def from_cache(request):
    if request.accepted_renderer.format != 'json':
        return None
    data = cache.get('api:' + request.get_full_path())
    if data is None:
        return None
    return Response(data, headers={'X-Cache': 'HIT'})


def save_to_cache(request, response):
    if request.accepted_renderer.format == 'json' and response.status_code == 200:
        cache.set('api:' + request.get_full_path(), response.data, timeout=settings.API_CACHE_TIMEOUT)
        response['X-Cache'] = 'MISS'
    return response


class CachedResponseMixin:
    def list(self, request, *args, **kwargs):
        cached = from_cache(request)
        if cached is not None:
            return cached
        response = super().list(request, *args, **kwargs)
        return save_to_cache(request, response)

    def retrieve(self, request, *args, **kwargs):
        cached = from_cache(request)
        if cached is not None:
            return cached
        response = super().retrieve(request, *args, **kwargs)
        return save_to_cache(request, response)
