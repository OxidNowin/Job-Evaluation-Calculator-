from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import JobEvaluation
from .forms import PostForm, UnlogicalPostForm
from .arrays import skills_arr, responsibility_arr, problems_solving_arr, union_arr, grade_arr

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
			hard_skills = str(form.cleaned_data['hard_skills'].upper())
			knowledge = str(form.cleaned_data['knowledge'].upper())
			soft_skills = str(form.cleaned_data['soft_skills'].upper())
			around_question = str(form.cleaned_data['around_question'].upper())
			question_complexity = str(form.cleaned_data['question_complexity'].upper())
			freedom_action = str(form.cleaned_data['freedom_action'].upper())
			nature_impact = str(form.cleaned_data['nature_impact'].upper())
			impact_importance = str(form.cleaned_data['impact_importance'].upper())

			"""Вычисления"""

			value_of_skills_section, is_skills_section_logical = compute_skills_section(hard_skills, knowledge, soft_skills)
			value_of_problems_section, is_problems_section_logical = compute_problems_section(around_question, question_complexity)
			value_of_union_section, is_union_of_sections_logical = compute_union_skills_and_problems(value_of_skills_section, value_of_problems_section)
			value_of_responsibility_section = compute_responsibility_section(freedom_action, nature_impact, impact_importance)

			"""Проверка на ненахождение соответствия"""

			if is_none(value_of_skills_section, value_of_problems_section, value_of_union_section, value_of_responsibility_section):
				return render(request, "evacalc/index.html", {'form': form,
					'error_message': 'Неккоректно ввели значения',})

			""" Суммирование значений """

			sum_of_values = value_of_skills_section + value_of_union_section + value_of_responsibility_section
			grade = grade_determine(sum_of_values)

			result_str = f"{value_of_skills_section} {int(value_of_problems_section*100)}% {value_of_union_section} {value_of_responsibility_section}  summa:{sum_of_values} grade:{grade}"

			jopa = {'title': title,
					'short_profile':short_profile,
					'value_of_skills_section': value_of_skills_section,
					'логично_1': is_skills_section_logical,
					'value_of_problems_section': f'{int(value_of_problems_section*100)} %',
					'логично_2': is_problems_section_logical,
					'value_of_union_section': value_of_union_section,
					'логично_3': is_union_of_sections_logical,
					'value_of_responsibility_section': value_of_responsibility_section,
					'sum_of_values': sum_of_values,
					'grade': grade}

			"""Проверка на логичность"""

			if (is_skills_section_logical and is_problems_section_logical and is_union_of_sections_logical) == False:
				return render(request, "evacalc/index.html", {'form': form,
					'logical_message': 'Нелогичность данных. Продолжить?',
					'jopa': jopa})

"""			j = JobEvaluation(
				title = title,
				user = request.user,
				short_profile = short_profile,
				hard_skills = hard_skills,
				knowledge = knowledge,
				soft_skills = soft_skills,
				value_of_skills_section = value_of_skills_section,
				around_question = around_question,
				question_complexity = question_complexity,
				value_of_problems_section = value_of_problems_section,
				value_of_union_section = value_of_union_section,
				freedom_action = freedom_action,
				nature_impact = nature_impact,
				impact_importance = impact_importance,
				value_of_responsibility_section = value_of_responsibility_section,
				sum_of_values = value_of_skills_section + value_of_union_section + value_of_responsibility_section,
				grade = grade)
			j.save()"""
			return render(request, 'evacalc/result.html', {'jopa':jopa})
		else:
			return render(request, 'evacalc/index.html',{'error_message':'Не указали наименование должности'})
	elif request.method == "POST" and 'unlogical_post' in request.POST:
		form = UnlogicalPostForm(request.POST)
		if form.is_valid():
			stroka = form.cleaned_data['unlogical_result']
			return HttpResponse(stroka)
	else:
		form = PostForm()
	return render(request, "evacalc/index.html", {'form': form})

def compute_skills_section(hard_skills, knowledge, soft_skills):

	"""
	Практические занятия
	Управленческие знания
	Навыки взаимодействия
	"""
	is_skills_section_logical = True

	for arr in skills_arr:
		if str(arr[0]) == hard_skills:
			if str(arr[1]) == knowledge:
				if str(arr[2]) == soft_skills:
					if str(arr[4]) == "0":
						is_skills_section_logical = False
					return int(arr[3]), is_skills_section_logical
	return None, None

def compute_problems_section(around_question, question_complexity):

	"""
	Область решаемых вопросов
	Сложность вопросов
	"""
	is_problems_section_logical = True

	for arr in problems_solving_arr:
		if str(arr[0]) == around_question:
			if str(arr[1]) == question_complexity:
				if str(arr[3]) == "0":
					is_problems_section_logical = False
				return float(arr[2]), is_problems_section_logical
	return None, None

def compute_union_skills_and_problems(value_of_skills_section, value_of_problems_section):

	is_union_of_sections_logical = True

	for arr in union_arr:
		if str(arr[0]) == str(value_of_problems_section):
			if str(arr[1]) == str(value_of_skills_section):
				if str(arr[3]) == "0":
					is_union_of_sections_logical = False
				return int(arr[2]), is_union_of_sections_logical
	return None, None

def compute_responsibility_section(freedom_action, nature_impact, impact_importance):

	"""
	Свобода действий
	Природа воздействия
	Важность воздействия
	"""

	for arr in responsibility_arr:
		if str(arr[0]) == freedom_action:
			if str(arr[1]) == nature_impact:
				if str(arr[2]) == impact_importance:
					return int(arr[3])
	return None

def grade_determine(sum_of_values):
	for summ in grade_arr:
		if (sum_of_values<=summ[2]) and (sum_of_values>=summ[1]):
			return summ[0]
	return None

def is_none(value_of_skills_section, value_of_problems_section, value_of_union_section, value_of_responsibility_section):
	if (value_of_skills_section == None) or (value_of_problems_section == None) or (value_of_union_section == None) or (value_of_responsibility_section == None):
		return True
	return False
