from django.db import models

# Create your models here.
class Mro(models.Model):
    name = models.CharField(
        'название МРО',
        max_length=50,
        null=True,
        blank=True
    )
    general = models.TextField(
        'общая инфа',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name