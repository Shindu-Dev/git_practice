# Generated by Django 3.0.8 on 2020-07-25 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FightScheduler', '0028_auto_20200723_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonboxerinfo',
            name='UserID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='User_ID_for_Additional_Non_Boxer_Info', to=settings.AUTH_USER_MODEL, verbose_name='User ID for Additional Non Boxer Info'),
        ),
    ]
