# Generated by Django 2.2.7 on 2021-03-07 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evacalc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobevaluation',
            name='around_question',
            field=models.CharField(max_length=1, verbose_name='Область решаемых вопросов'),
        ),
        migrations.AlterField(
            model_name='jobevaluation',
            name='freedom_action',
            field=models.CharField(max_length=1, verbose_name='Свобода действий'),
        ),
        migrations.AlterField(
            model_name='jobevaluation',
            name='hard_skills',
            field=models.CharField(max_length=1, verbose_name='Практические знания'),
        ),
        migrations.AlterField(
            model_name='jobevaluation',
            name='nature_impact',
            field=models.CharField(max_length=1, verbose_name='Природа воздействия'),
        ),
        migrations.AlterField(
            model_name='jobevaluation',
            name='question_complexity',
            field=models.CharField(max_length=1, verbose_name='Сложность вопросов'),
        ),
        migrations.AlterField(
            model_name='jobevaluation',
            name='soft_skills',
            field=models.CharField(max_length=1, verbose_name='Навыки взаимодействия'),
        ),
    ]
