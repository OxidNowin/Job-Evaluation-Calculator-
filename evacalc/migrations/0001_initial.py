# Generated by Django 2.2.7 on 2021-03-07 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Название должности')),
                ('short_profile', models.CharField(default='', max_length=2, verbose_name='Краткий профиль')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('hard_skills', models.CharField(max_length=2, verbose_name='Практические знания')),
                ('knowledge', models.CharField(max_length=2, verbose_name='Управленческие знания')),
                ('soft_skills', models.CharField(max_length=2, verbose_name='Навыки взаимодействия')),
                ('value_of_skills_section', models.IntegerField(default=0, verbose_name='Значение знания')),
                ('around_question', models.CharField(max_length=2, verbose_name='Область решаемых вопросов')),
                ('question_complexity', models.CharField(max_length=2, verbose_name='Сложность вопросов')),
                ('value_of_problems_section', models.IntegerField(default=0, verbose_name='Процент решения проблем')),
                ('value_of_union_section', models.IntegerField(default=0, verbose_name='Значение оценки')),
                ('freedom_action', models.CharField(max_length=2, verbose_name='Свобода действий')),
                ('nature_impact', models.CharField(max_length=2, verbose_name='Природа воздействия')),
                ('impact_importance', models.CharField(max_length=2, verbose_name='Важность воздействия')),
                ('value_of_responsibility_section', models.IntegerField(default=0, verbose_name='Оценка воздействия')),
                ('sum_of_values', models.IntegerField(default=0, verbose_name='Сумма значений')),
                ('grade', models.IntegerField(default=0, verbose_name='Грейд')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
