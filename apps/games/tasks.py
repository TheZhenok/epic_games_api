from settings.celery import app
from django.db.models import F

from games.models import Game, Subscribe


@app.task
def do_test(game_id: int, *args, **kwargs):
    Game.objects.filter(id=game_id).update(
        price=F('price') + 10
    )
    print("OK")


@app.task
def cancel_subcribe(subcribe_id: int, *args, **kwargs) -> None:
    Subscribe.objects.filter(id=subcribe_id).update(is_active=False)
