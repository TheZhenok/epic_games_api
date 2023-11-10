from rest_framework.pagination import PageNumberPagination


class MyLimitPaginator(PageNumberPagination):
    page_size = 10
    page_query_param = "p"
    max_page_size = 100
