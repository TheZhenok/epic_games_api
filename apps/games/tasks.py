# Python
import random
from typing import Any

# Django
from django.db.models import (
    F,
    query
)

# First party
from games.models import (
    Game,
    Subscribe
)
from settings.celery import app


@app.task(name='games-price-updater')
def games_price_updater() -> None:
    """Воркер для авто-обновления цен играм."""

    def random_value() -> int:
        return random.randrange(1, 20)

    games: query.QuerySet[Game] = \
        Game.objects.filter(
            is_hidden=False
        )
    game: Game
    for game in games:
        game.price += random_value()
        game.save(update_fields=('price',))

    print(f'All games prices were updated !!!')


@app.task(name='test-worker')
def test_worker(
    game_id: int,
    *args: Any,
    **kwargs: Any
):
    Game.objects.filter(
        id=game_id
    ).update(
        price=F('price') + 10
    )
    print(f'Game: {game_id} price was updated')


@app.task
def cancel_subcribe(
    subcribe_id: int,
    *args: Any,
    **kwargs: Any
) -> None:
    Subscribe.objects.filter(
        id=subcribe_id
    ).update(
        is_active=False
    )
