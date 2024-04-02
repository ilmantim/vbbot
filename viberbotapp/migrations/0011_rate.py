# Generated by Django 5.0.3 on 2024-04-02 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viberbotapp', '0010_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Обозначение')),
                ('id_tariff', models.IntegerField(verbose_name='ID тарифа')),
                ('id_indication', models.IntegerField(verbose_name='ID показания')),
                ('registration_date', models.DateTimeField(verbose_name='Дата приёма')),
                ('readings', models.IntegerField(verbose_name='Показания счетчика')),
                ('cost', models.FloatField(verbose_name='Стоимость')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='viberbotapp.device', verbose_name='Устройство')),
            ],
        ),
    ]
