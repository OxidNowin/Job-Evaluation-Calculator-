# Generated by Django 2.2.7 on 2021-03-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacalc', '0006_delete_jobevaluationxl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobevaluation',
            name='impact_importance',
            field=models.CharField(max_length=3, verbose_name='Важность воздействия'),
        ),
        migrations.AlterField(
            model_name='jobevaluation',
            name='knowledge',
            field=models.CharField(max_length=3, verbose_name='Управленческие знания'),
        ),
    ]
