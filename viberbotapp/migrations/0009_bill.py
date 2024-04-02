# Generated by Django 5.0.3 on 2024-04-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viberbotapp', '0008_alter_person_context'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(verbose_name='номер лицевого счета')),
                ('persons', models.ManyToManyField(related_name='bills', to='viberbotapp.person', verbose_name='клиенты')),
            ],
        ),
    ]
