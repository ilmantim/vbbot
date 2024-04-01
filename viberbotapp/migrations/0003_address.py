# Generated by Django 5.0.3 on 2024-04-01 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viberbotapp', '0002_remove_person_step_person_state_alter_person_chat_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='детализированная инфа')),
                ('num', models.IntegerField(verbose_name='номер кнопки')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='viberbotapp.mro', verbose_name='связь с МРО')),
            ],
        ),
    ]
