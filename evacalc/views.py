from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import JobEvaluation
from .forms import PostForm, UnlogicalPostForm
from .arrays import skills_arr, responsibility_arr, probl_solv_arr, check_arr, grade_arr


@login_required
def result(request):
	return render(request, 'evacalc/result.html')

@login_required
def index(request):
	if request.method == "POST" and 'logical_post' in request.POST:
		form = PostForm(request.POST)
		if form.is_valid():

			"""Считывание данных"""

			title = form.cleaned_data['title'].title()
			short_profile = form.cleaned_data['short_profile']
			tech_skills = str(form.cleaned_data['tech_skills'].upper())
			knowledge = str(form.cleaned_data['knowledge'].upper())
			soft_skills = str(form.cleaned_data['soft_skills'].upper())
			around_question = str(form.cleaned_data['around_question'].upper())
			question_diff = str(form.cleaned_data['question_diff'].upper())
			free_move = str(form.cleaned_data['free_move'].upper())
			nature = str(form.cleaned_data['nature'].upper())
			impact_importance = str(form.cleaned_data['impact_importance'].upper())

			"""Вычисления"""

			value, logical_1 = ski_and_kno(tech_skills, knowledge, soft_skills)
			value_perc, logical_2 = troubles_sol(around_question, question_diff)
			eva_value, logical_3 = union_skills_and_solving(value, value_perc)
			eva_resp = responsibility(free_move, nature, impact_importance)

			"""Проверка на ненахождение соответствия"""

			if none_check(value, value_perc, eva_value, eva_resp) == False:
				return render(request, "evacalc/index.html", {'form': form,
					'error_message': 'Неккоректно ввели значения',})

			"""Проверка на ВОДОПАД"""

			if waterfall_check(tech_skills, around_question, free_move) == False:
				return render(request, "evacalc/index.html", {'form': form,
					'error_message': 'Не соблюден принцип водопада',})				

			sum_of_values = value + eva_value + eva_resp
			grade = grade_determine(sum_of_values)

			result_str = f"{value} {int(value_perc*100)}% {eva_value} {eva_resp}  summa:{sum_of_values} grade:{grade}"

			"""Проверка на логичность"""

			if (logical_1 and logical_2 and logical_3):
				return render(request, "evacalc/index.html", {'form': form,
					'logical_message': 'Нелогичность данных. Продолжить?',
					'jopa': result_str,})				

			jopa = {'title': title,
					'short_profile':short_profile,
					'value': value,
					'логично_1': logical_1,
					'value_perc': f'{int(value_perc*100)} %',
					'логично_2': logical_2,
					'eva_value': eva_value,
					'логично_3': logical_3,
					'eva_resp': eva_resp,
					'sum_of_values': sum_of_values,
					'grade': grade}
			"""j = JobEvaluation(
				title = title,
				user = request.user,
				short_profile = short_profile,
				tech_skills = tech_skills,
				knowledge = knowledge,
				soft_skills = soft_skills,
				value = value,
				around_question = around_question, 
				question_diff = question_diff,
				value_perc = value_perc,
				eva_value = eva_value,
				free_move = free_move,
				nature = nature,
				impact_importance = impact_importance, 
				eva_resp = eva_resp,
				sum_of_values = value + eva_value + eva_resp)
			j.save()"""
			return render(request, 'evacalc/result.html', {'jopa':jopa})	
	elif request.method == "POST" and 'unlogical_post' in request.POST:
		form = UnlogicalPostForm(request.POST)
		if form.is_valid():
			stroka = form.cleaned_data['unlogical_result']
			return HttpResponse(stroka)
	else:
		form = PostForm()	
	return render(request, "evacalc/index.html", {'form': form})

def ski_and_kno(tech_skills, knowledge, soft_skills):
	
	"""
	Практические занятия
	Управленческие знания
	Навыки взаимодействия
	"""
	logical_1 = True
	
	for arr in skills_arr:
		if str(arr[0]) == tech_skills:
			if str(arr[1]) == knowledge:
				if str(arr[2]) == soft_skills:
					if str(arr[4]) == "0":
						logical_1 = False
					return int(arr[3]), logical_1
	return None, None

def troubles_sol(around_question, question_diff):

	"""
	Область решаемых вопросов
	Сложность вопросов
	"""
	logical_2 = True

	for arr in probl_solv_arr:
		if str(arr[0]) == around_question:
			if str(arr[1]) == question_diff:
				if str(arr[3]) == "0":
					logical_2 = False
				return float(arr[2]), logical_2
	return None, None

def union_skills_and_solving(value, value_perc):

	logical_3 = True

	for arr in check_arr:
		if str(arr[0]) == str(value_perc):
			if str(arr[1]) == str(value):
				if str(arr[3]) == "0":
					logical_3 = False
				return int(arr[2]), logical_3
	return None, None

def responsibility(free_move, nature, impact_importance):

	"""
	Свобода действий
	Природа воздействия
	Важность воздействия
	"""

	for arr in responsibility_arr:
		if str(arr[0]) == free_move:
			if str(arr[1]) == nature:
				if str(arr[2]) == impact_importance:
					return int(arr[3])
	return None

def grade_determine(sum_of_values):
	for summ in grade_arr:
		if (sum_of_values<=summ[2]) and (sum_of_values>=summ[1]):
			return summ[0]
	return None 

def none_check(value, value_perc, eva_value, eva_resp):
	if (value == None) or (value_perc == None) or (eva_value == None) or (eva_resp == None):
		return False
	return True

def waterfall_check(tech_skills,around_question, free_move):
	if ord(tech_skills) < ord(around_question):
		return False
	elif ord(around_question) < ord(free_move):
		return False
	return True
