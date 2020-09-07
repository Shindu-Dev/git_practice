# Generated by Django 3.0.8 on 2020-07-23 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FightScheduler', '0022_auto_20200722_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonboxerinfo',
            name='boxingOntarionEmployeeNum',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nonboxerinfo',
            name='coachLevel',
            field=models.CharField(choices=[('1', '1 - Certified Apprentice Coach'), ('2', '2 - Certified Club Coach'), ('3', '3 - Competition Coach'), ('4', '4 - Advanced Coaching Diploma I'), ('5', '5 - Advanced Coaching Diploma II')], default='1', max_length=30),
        ),
        migrations.AlterField(
            model_name='nonboxerinfo',
            name='officialLevel',
            field=models.CharField(choices=[('1', '1 - Regional I'), ('2', '2 - Regional II'), ('3', '3 - Provincial'), ('4', '4 - National')], default='1', max_length=30),
        ),
    ]