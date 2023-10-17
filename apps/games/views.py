# Python
from typing import Optional

# DRF
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response as JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    IsAuthenticated
)
from django.core.exceptions import ValidationError

# First party
from abstracts.mixins import (
    ObjectMixin,
    ResponseMixin
)
from games.models import Game, Subscribe
from games.serializers import (
    GameCreateSerializer,
    GameSerializer
)


class GameViewSet(ResponseMixin, ObjectMixin, ViewSet):
    """
    ViewSet for Game model.
    """
    queryset = Game.objects.all()
    permission_classes = [IsAuthenticated]

    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> JsonResponse:
        serializer: GameSerializer = \
            GameSerializer(
                instance=self.queryset,
                many=True
            )
        return self.json_response(serializer.data)

    def retrieve(
        self,
        request: Request,
        pk: Optional[int] = None
    ) -> JsonResponse:
        game = self.get_object(self.queryset, pk)
        serializer: GameSerializer = \
            GameSerializer(instance=game)

        return self.json_response(serializer.data)

    def create(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> JsonResponse:
        serializer: GameCreateSerializer = \
            GameCreateSerializer(
                data=request.data
            )
        serializer.is_valid(
            raise_exception=True
        )
        game: Game = serializer.save()

        return self.json_response(f'{game.name} is created. ID: {game.id}')

    def update(
        self,
        request: Request,
        pk: str
    ) -> JsonResponse:
        game = self.get_object(self.queryset, pk)
        serializer: GameSerializer = \
            GameSerializer(
                instance=game,
                data=request.data
            )
        if not serializer.is_valid():
            return self.json_response(
                f'{game.name} wasn\'t updated', 'Warning'
            )
        serializer.save()
        return self.json_response(f'{game.name} was updated')

    def partial_update(
        self,
        request: Request,
        pk: str
    ) -> JsonResponse:
        game = self.get_object(self.queryset, pk)
        serializer: GameSerializer = \
            GameSerializer(
                instance=game,
                data=request.data,
                partial=True
            )
        if not serializer.is_valid():
            return self.json_response(
                f'{game.name} wasn\'t partially-updated', 'Warning'
            )
        serializer.save()
        return self.json_response(f'{game.name} was partially-updated')

    def destroy(
        self,
        request: Request,
        pk: str
    ) -> JsonResponse:
        # TODO: мы будем проставлять
        #       ей статус 'datetime_deleted'
        #
        game = self.get_object(self.queryset, pk)
        name: str = game.name
        game.delete()

        return self.json_response(f'{name} was deleted')

    @action(
        methods=['POST'],
        detail=False,
        url_path='sub/(?P<pk>[^/.]+)'
    )
    def subscribe(self, request: Request, pk: int = None) -> JsonResponse:
        game = self.get_object(
            queryset=Game.objects.all(),
            obj_id=pk
        )
        sub = Subscribe.objects.create(
            user=request.user,
            is_active=True,
            game=game
        )
        return self.json_response(
            data={
                "message": {
                    "game_id": game.id,
                    "subscribe_id": sub.id,
                    "date_finished": sub.datetime_finished
                }
            }
        )
