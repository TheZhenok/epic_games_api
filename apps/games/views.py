# Python
from typing import Optional
from datetime import datetime

# DRF
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response as JsonResponse
from rest_framework.viewsets import ViewSet

# Django
from django.db.models import query

# First party
from abstracts.mixins import (
    ObjectMixin,
    ResponseMixin
)
from games.models import (
    Game,
    Subscribe
)
from games.serializers import (
    GameCreateSerializer,
    GameSerializer
)
from games.tasks import (
    cancel_subcribe,
    test_worker
)

# Local
from .permissions import GamePermission


class GameViewSet(ResponseMixin, ObjectMixin, ViewSet):
    """
    ViewSet for Game model.
    """
    permission_classes = (
        GamePermission,
    )
    queryset = Game.objects.all()

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
        detail=False
    )
    def show_hidden_games(self, request: Request) -> JsonResponse:
        hidden_games: query.QuerySet = \
            Game.objects.filter(is_hidden=True)

        serializer: GameSerializer = \
            GameSerializer(
                instance=hidden_games,
                many=True
            )
        return self.json_response(serializer.data)

    @action(
        methods=['POST'],
        detail=False,
        url_path='sub/game/(?P<pk>[^/.]+)'
    )
    def subscribe(self, request: Request, pk: int = None) -> JsonResponse:
        CANCEL_TIMEOUT_30_DAYS = 30 * 24 * 60 * 60

        game = self.get_object(
            queryset=Game.objects.all(),
            obj_id=pk
        )
        sub = Subscribe.objects.create(
            user=request.user,
            is_active=True,
            game=game
        )
        cancel_subcribe.apply_async(
            kwargs={
                'subcribe_id': sub.id
            },
            countdown=CANCEL_TIMEOUT_30_DAYS
        )
        return self.json_response(
            data={
                'message': {
                    'game_id': game.id,
                    'subscribe_id': sub.id,
                    'date_finished': sub.datetime_finished
                }
            }
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path='sub/check/(?P<pk>[^/.]+)'
    )
    def check_subcribe(self, request: Request, pk: int = None):
        test_worker.apply_async(
            kwargs={'game_id': pk},
            countdown=10
        )
        return self.json_response(
            data={'message': 'ok'}
        )
