# Python
import random
from typing import Any

# Django
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager,
    User
)
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    """GENERATE ALL."""

    help = "Closes the specified poll for voting"

    def _generate_users(self) -> bool:
        def _generate_username() -> str:
            letters: str = 'qwertyuiopasdfghjklzxcvbnm_'
            return "".join([random.choice(letters) for _ in range(10)])
        
        def _generate_email_domain() -> str:
            domains: list[str] = [
                'yandex.ru', 'gmail.com', 'mail.ru',
                'bk.ru', 'yahoo.com', 'hotmail.com',
                'ok.ru', 'tempmail.com', 'cloud.com'
            ]
            return "@" + random.choice(domains)

        TOTAL_USERS_COUNT = 50000
        CURRENT_USERS_COUNT = User.objects.all().count()
        try:
            for i in range(CURRENT_USERS_COUNT, TOTAL_USERS_COUNT):
                username = _generate_username()
                password = "qwerty"
                email = username + _generate_email_domain()
                user = User(
                    username=User.normalize_username(username),
                    password=make_password(password),
                    email=BaseUserManager.normalize_email(email)
                )
                try:
                    user.save()
                    print(i)
                except IntegrityError:
                    continue
        except:
            print(User.objects.all().count())
            return False

    def handle(self, *args: Any, **options: Any) -> str:
        self._generate_users()
        return "OK"
