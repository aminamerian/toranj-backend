from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
