# DRF
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList


class UserPageNumberPaginator(PageNumberPagination):
    """
    Пагинатор для вывода пользователей.

    Параметры:
        - page_size_query_param:
        Параметр для того чтоб указывать сколько нужно вывести элементов

        - page_query_param:
        Параметр для того чтоб указывать нумерацию страницы

        - max_page_size:
        сколько максимум можно вывести элементов

        - page_size:
        по стандарту сколько будет элементов

    Пример запроса:
        /user/?page=2&size=10
    """
    page_size_query_param: str = 'size'
    page_query_param: str = 'page'
    max_page_size: int = 5
    page_size: int = 4

    def get_paginated_response(
        self,
        data: ReturnList
    ) -> Response:
        response: Response = \
            Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link(),
                        'pages': self.page.paginator.num_pages,
                        'count': self.page.paginator.count
                    },
                    'results': data
                }
            )
        return response


class UserLimitOffsetPaginator(LimitOffsetPagination):
    """
    Description.
    """
    offset: int = 0
    limit: int = 2

    def get_paginated_response(
        self,
        data: ReturnList
    ) -> Response:
        response: Response = \
            Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link()
                    },
                    'results': data
                }
            )
        return response
