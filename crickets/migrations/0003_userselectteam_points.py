# Generated by Django 3.2.13 on 2022-05-18 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0002_auto_20220518_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='userselectteam',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
