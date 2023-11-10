from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.core.mail import send_mail

from games.models import Game


@receiver(post_save, sender=Game)
def span_attack_when_create_new_game(
    sender: Game.__class__, 
    instance: Game, 
    craeted: bool, 
    **kwargs
) -> None:
    emails: list[str] = User.objects.all().values_list('email', flat=True)
    send_mail(
        subject='EPIC GAMES! NEW GAME!',
        message='Вышла новая игра, иди купи!',
        from_email='zhenok1109@gmail.com',
        recipient_list=emails
    )

