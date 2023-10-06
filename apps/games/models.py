# Django
from django.core.validators import MinValueValidator
from django.db import models


class Game(models.Model):
    """MY GAME!"""

    name: str = models.CharField(
        verbose_name='игра',
        max_length=200
    )
    price: float = models.DecimalField(
        verbose_name='цена',
        max_digits=11,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message='Мы деньги за игры не даём!')
        ]
    )
    poster: str = models.ImageField(
        verbose_name='постер',
        upload_to='posters'
    )
    rate: float = models.FloatField(
        verbose_name='рейтинг',
        max_length=5
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'игра'
        verbose_name_plural = 'игры'

    def __str__(self) -> str:
        return f'{self.name} | {self.price:.2f}$'


# Создать форму для создания игры и редактирования игры
# Реализовать создание и удаление игры
