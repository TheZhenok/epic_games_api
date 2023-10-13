# Python
from typing import Any

# DRF
from rest_framework.response import Response as JsonResponse
from rest_framework.validators import ValidationError

# Django
from django.db.models import query


class ObjectMixin:
    """Абстрактный вспомогательный класс для объектов."""

    def get_object(
        self,
        queryset: query.QuerySet,
        obj_id: str
    ) -> Any:
        """Метод для вытаскивания объекта."""

        obj: Any = queryset.filter(id=obj_id).first()
        if obj is None:
            raise ValidationError(
                {
                    'status': 'Error',
                    'results': f'Object {obj_id} not found'
                }
            )
        return obj


class ResponseMixin:
    """Абстрактный вспомогательный класс для респонсов."""

    STATUS_SUCCESS: str = 'Success'
    STATUS_WARNING: str = 'Warning'
    STATUS_ERROR: str = 'Error'
    STATUSES: tuple[str, ...] = (
        STATUS_SUCCESS,
        STATUS_WARNING,
        STATUS_ERROR
    )

    def json_response(
        self,
        data: Any,
        status: str = STATUS_SUCCESS
    ) -> JsonResponse:

        if status not in self.STATUSES:
            raise ValidationError('FATAL ERROR')

        return JsonResponse(
            {
                'status': status,
                'results': data
            }
        )
