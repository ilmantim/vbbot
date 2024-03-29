from django.db import models


class Person(models.Model):
    chat_id = models.CharField(
        verbose_name='id персоны',
        max_length=50
    )
    name = models.CharField(
        verbose_name='имя персоны',
        max_length=50
    )
    step = models.IntegerField(
        verbose_name='позиция персоны'
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
