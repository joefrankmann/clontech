"""Project-specific paginators."""
import rest_framework.pagination


class FlexiblePageNumberPagination(rest_framework.pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 250
    page_size = 250