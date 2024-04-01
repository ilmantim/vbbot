from django.db import models


class Person(models.Model):
    chat_id = models.CharField(
        verbose_name='id юзера',
        max_length=50
    )
    name = models.CharField(
        verbose_name='имя юзера',
        max_length=50
    )
    state = models.PositiveIntegerField(
        verbose_name='позиция юзера в диалоге',
        default=0
    )


class Mro(models.Model):
    name = models.CharField(
        'название МРО',
        max_length=50,
    )
    general = models.TextField(
        verbose_name='общая информация',
    )

    def __str__(self):
        return self.name
