# Generated by Django 3.2.13 on 2022-05-20 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0015_auto_20220519_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampointscal',
            name='all',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teampointscal',
            name='bat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teampointscal',
            name='bowl',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teampointscal',
            name='wk',
            field=models.IntegerField(default=0),
        ),
    ]