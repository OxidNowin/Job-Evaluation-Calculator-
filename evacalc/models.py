from django.db import models
from django.utils import timezone

class JobEvaluation(models.Model):
	user = models.ForeignKey('account.MyUser', on_delete=models.CASCADE)
	title = models.CharField("Название должности",max_length=25)
	short_profile = models.CharField("Краткий профиль",max_length=2)
	created_date = models.DateTimeField(default=timezone.now)
	hard_skills = models.CharField("Практические знания", max_length=1)
	knowledge = models.CharField("Управленческие знания", max_length=2)
	soft_skills = models.CharField("Навыки взаимодействия", max_length=1)
	value_of_skills_section = models.IntegerField("Значение знания", default=0)
	around_question = models.CharField("Область решаемых вопросов", max_length=1)
	question_complexity = models.CharField("Сложность вопросов", max_length=1)
	value_of_problems_section = models.IntegerField("Процент решения проблем", default=0)
	value_of_union_section = models.IntegerField("Значение оценки", default=0)
	freedom_action = models.CharField("Свобода действий", max_length=1)
	nature_impact = models.CharField("Природа воздействия", max_length=1)
	impact_importance = models.CharField("Важность воздействия", max_length=2)
	value_of_responsibility_section = models.IntegerField("Оценка воздействия", default=0)
	sum_of_values = models.IntegerField("Сумма значений", default=0)
	grade = models.IntegerField("Грейд", default=0)

	def __str__(self):
		return self.title
