# Generated by Django 5.0.3 on 2024-04-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viberbotapp', '0006_person_context'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='context',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Контекст юзера'),
        ),
    ]
