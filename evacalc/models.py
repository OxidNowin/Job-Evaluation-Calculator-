from django.db import models
from django.utils import timezone

class JobEvaluation(models.Model):
	user = models.ForeignKey('account.MyUser', on_delete=models.CASCADE)
	title = models.CharField("Название должности",max_length=25)
	created_date = models.DateTimeField(default=timezone.now)
	tech_skills = models.CharField("Практические знания", max_length=2)
	knowledge = models.CharField("Управленческие знания", max_length=2)
	soft_skills = models.CharField("Навыки взаимодействия", max_length=2)
	value = models.IntegerField("Значение знания", default=0)
	around_question = models.CharField("Область решаемых вопросов", max_length=2)
	question_diff = models.CharField("Сложность вопросов", max_length=2)
	value_perc = models.IntegerField("Процент решения проблем", default=0)
	eva_value = models.IntegerField("Значение оценки", default=0)
	free_move = models.CharField("Свобода действий", max_length=2)
	nature = models.CharField("Природа воздействия", max_length=2)
	impact_importance = models.CharField("Важность воздействия", max_length=2)
	eva_resp = models.IntegerField("Оценка воздействия", default=0)
	sum_of_values = models.IntegerField("Сумма значений", default=0)
	grade = models.IntegerField("Грейд", default=0)

	def __str__(self):
		return self.title	