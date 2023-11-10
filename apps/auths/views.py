# DRF
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Django
from django.contrib.auth.models import User

# First party
from abstracts.mixins import ResponseMixin
from auths.paginators import (
    UserLimitOffsetPaginator,
    UserPageNumberPaginator
)
from auths.serializers import UserSerializerAll


class UserViewSet(ResponseMixin, ModelViewSet):
    serializer_class = UserSerializerAll
    pagination_class = UserPageNumberPaginator
    queryset = User.objects.all()

    @action(
        methods=['get'],
        detail=False,
        url_path='paginator-page-number',
        permission_classes=(AllowAny,)
    )
    def paginator_page_number(self, request: Request) -> Response:

        paginator: UserPageNumberPaginator = \
            self.pagination_class()

        objects: list = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: UserSerializerAll = \
            UserSerializerAll(
                objects,
                many=True
            )
        return self.json_response(
            serializer.data,
            paginator=paginator
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='paginator-limit-offset',
        permission_classes=(AllowAny,)
    )
    def paginator_limit_offset(self, request: Request) -> Response:

        paginator: UserLimitOffsetPaginator = \
            UserLimitOffsetPaginator()

        objects: list = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: UserSerializerAll = \
            UserSerializerAll(
                objects,
                many=True
            )
        return self.json_response(
            serializer.data,
            paginator=paginator
        )
