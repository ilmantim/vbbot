# Generated by Django 5.0.3 on 2024-04-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viberbotapp', '0005_auto_20240401_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='context',
            field=models.CharField(max_length=100, null=True, verbose_name='Контекст юзера'),
        ),
    ]
