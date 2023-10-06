from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 20


class PaginationForBlog(pagination.PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 10
