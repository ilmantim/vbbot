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
    context = models.TextField(
        verbose_name='Контекст юзера',
        null=True,
        blank=True
    )
    details = models.TextField(
        verbose_name='Второй контекст юзера',
        null=True,
        blank=True
    )
    prev_step = models.PositiveIntegerField(
        verbose_name='Предыдущий шаг',
        null=True,
        blank=True
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


class Address(models.Model):
    name = models.TextField(
        verbose_name='детализированная инфа',
    )
    department = models.ForeignKey(
        Mro,
        verbose_name='связь с МРО',
        on_delete=models.CASCADE,
        related_name='addresses',
        null=True
    )
    num = models.IntegerField(
        verbose_name='номер кнопки',
    )

    def __str__(self):
        return self.name


class Bill(models.Model):
    persons = models.ManyToManyField(
        Person,
        verbose_name='клиенты',
        related_name='bills'
    )
    value = models.IntegerField(
        verbose_name='номер лицевого счета'
    )


class Device(models.Model):
    address = models.TextField(
        verbose_name='адрес счета'
    )
    device_title = models.TextField(
        verbose_name='Прибор учета'
    )
    modification = models.TextField(
        verbose_name='Модификация прибора учета'
    )
    serial_number = models.TextField(
        verbose_name='Серийный номер прибора учета'
    )
    id_device = models.IntegerField(
        verbose_name='ID счетчика'
    )
    bill = models.ForeignKey(
        Bill,
        verbose_name='Лицевой счет',
        on_delete=models.CASCADE,
        related_name='devices'
    )


class Rate(models.Model):
    title = models.CharField(
        'Обозначение',
        max_length=20,
        null=True
    )
    id_tariff = models.IntegerField(
        verbose_name='ID тарифа',
        null=True
    )
    id_indication = models.IntegerField(
        verbose_name='ID показания',
        null=True
    )
    registration_date = models.DateTimeField(
        verbose_name='Дата приёма',
        null=True
    )
    readings = models.IntegerField(
        verbose_name='Показания счетчика',
        null=True
    )
    device = models.ForeignKey(
        Device,
        verbose_name='Устройство',
        on_delete=models.CASCADE,
        related_name='rates'
    )
    cost = models.FloatField(
        verbose_name='Стоимость',
        null=True
    )


class Favorite(models.Model):
    person = models.ForeignKey(
        Person,
        verbose_name='юзер избранного ЛС',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    bill = models.ForeignKey(
        Bill,
        verbose_name='Избранный ЛС',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
