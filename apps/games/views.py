from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from games.models import Game
from games.serializers import GameSerializer


class GameViewSet(viewsets.ViewSet):
    """
    ViewSet for Game model.
    """

    queryset = Game.objects.all()

    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        serializer: GameSerializer = GameSerializer(
            instance=self.queryset, many=True
        )
        return Response(
            data=serializer.data
        )
    
    def retrieve(
        self, 
        request: Request, 
        pk: int = None
    ) -> Response:
        try:
            game = self.queryset.get(pk=pk)
        except Game.DoesNotExist:
            raise ValidationError('Object not found!', code=404)
        
        serializer = GameSerializer(instance=game)
        return Response(data=serializer.data)
