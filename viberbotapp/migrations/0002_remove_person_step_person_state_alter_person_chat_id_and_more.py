# Generated by Django 5.0.3 on 2024-03-30 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viberbotapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='step',
        ),
        migrations.AddField(
            model_name='person',
            name='state',
            field=models.PositiveIntegerField(default=0, verbose_name='позиция юзера в диалоге'),
        ),
        migrations.AlterField(
            model_name='person',
            name='chat_id',
            field=models.CharField(max_length=50, verbose_name='id юзера'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=50, verbose_name='имя юзера'),
        ),
    ]
