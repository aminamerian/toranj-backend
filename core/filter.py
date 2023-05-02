from rest_framework import filters
from django.db.models import Q


class ProductListFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        category_id = request.query_params.get('category_id')
        price__lt = request.query_params.get('price__lt')
        price__gt = request.query_params.get('price__gt')
        is_available = request.query_params.get('is_available')

        if category_id is not None:
            queryset = queryset.filter(Q(category_id=category_id) |
                                       Q(category__parent_id=category_id) |
                                       Q(category__parent__parent_id=category_id))
        if price__lt is not None:
            queryset = queryset.filter(price__lt=price__lt)

        if price__gt is not None:
            queryset = queryset.filter(price__gt=price__gt)

        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')

        return queryset
