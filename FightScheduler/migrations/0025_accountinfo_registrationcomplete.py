# Generated by Django 3.0.8 on 2020-07-23 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FightScheduler', '0024_auto_20200723_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountinfo',
            name='registrationComplete',
            field=models.BooleanField(default=False),
        ),
    ]
