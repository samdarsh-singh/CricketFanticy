# Generated by Django 3.2.13 on 2022-05-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0013_alter_fantasypoints_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userselectteam',
            name='user_team_id',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]