# Generated by Django 3.2.13 on 2022-05-19 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0008_auto_20220518_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchlist',
            name='timeleft',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]