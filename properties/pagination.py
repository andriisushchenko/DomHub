from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class SkipLimitPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    offset_query_param = 'skip'

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'skip': self.offset,
            'limit': self.limit,
            'nextLink': self.get_next_link(),
            'previousLink': self.get_previous_link(),
            'results': data,
        })
