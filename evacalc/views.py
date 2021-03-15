from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import JobEvaluation
from .forms import PostForm, UnlogicalPostForm
from .arrays import skills_arr, responsibility_arr, problems_solving_arr, union_arr, grade_arr

import xlsxwriter


@login_required
def archive_date(request):
    if request.method == "POST":
        job_dict = request.POST
        job_id = list(job_dict.values())[1]
        redirect_str = "archive_date"
        delete_job_evaluation(job_id, redirect_str)
    jobs_list = JobEvaluation.objects.order_by('-created_date').filter(user=request.user)
    context = {'jobs_list': jobs_list}
    return render(request, 'evacalc/archive.html', context)


@login_required
def archive_grade(request):
    if request.method == "POST":
        job_dict = request.POST
        job_id = list(job_dict.values())[1]
        redirect_str = "archive_grade"
        delete_job_evaluation(job_id, redirect_str)
    jobs_list = JobEvaluation.objects.order_by('-grade').filter(user=request.user)
    context = {'jobs_list': jobs_list}
    return render(request, 'evacalc/archive.html', context)


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

            value_of_skills_section, is_skills_section_logical = compute_skills_section(hard_skills, knowledge,
                                                                                        soft_skills)
            value_of_problems_section, is_problems_section_logical = compute_problems_section(around_question,
                                                                                              question_complexity)
            value_of_union_section, is_union_of_sections_logical = compute_union_skills_and_problems(
                value_of_skills_section, value_of_problems_section)
            value_of_responsibility_section = compute_responsibility_section(freedom_action, nature_impact,
                                                                             impact_importance)

            """Проверка на ненахождение соответствия"""

            if is_none(value_of_skills_section, value_of_problems_section, value_of_union_section,
                       value_of_responsibility_section):
                return render(request, "evacalc/index.html", {'form': form,
                                                              'error_message': 'Неккоректно ввели значения', })

            if is_waterfall_principle(hard_skills, around_question, freedom_action) is False:
                return render(request, "evacalc/index.html", {'form': form,
                                                              'error_message': 'Не соблюден принцип водопада', })

            """ Суммирование значений """

            sum_of_values = value_of_skills_section + value_of_union_section + value_of_responsibility_section
            grade = grade_determine(sum_of_values)

            result_str = f"{request.user} {title} {short_profile} {hard_skills} {knowledge} {soft_skills} {value_of_skills_section} {around_question} {question_complexity} {int(value_of_problems_section * 100)} {value_of_union_section} {freedom_action} {nature_impact} {impact_importance} {value_of_responsibility_section} {sum_of_values} {grade} "

            """Проверка на логичность"""

            if (is_skills_section_logical and is_problems_section_logical and is_union_of_sections_logical) is False:
                return render(request, "evacalc/index.html", {'form': form,
                                                              'logical_message': 'Нелогичность данных. Продолжить?',
                                                              'result_str': result_str})
            try:
                save_model(
                    title,
                    request.user,
                    short_profile,
                    hard_skills,
                    knowledge,
                    soft_skills,
                    value_of_skills_section,
                    around_question,
                    question_complexity,
                    int(value_of_problems_section * 100),
                    value_of_union_section,
                    freedom_action,
                    nature_impact,
                    impact_importance,
                    value_of_responsibility_section,
                    value_of_skills_section + value_of_union_section + value_of_responsibility_section,
                    grade)
            except:
                return render(request, "evacalc/index.html", {'form': form,
                                                              'error_message': 'Неккоректно ввели значения', })
            form = PostForm()
            return render(request, 'evacalc/index.html', {'form': form,
                                                          'success': result_str})
        else:
            return render(request, 'evacalc/index.html', {'form': form,
                                                          'error_message': 'Не указали наименование должности'})
    elif request.method == "POST" and 'unlogical_post' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            result_str = form.cleaned_data['unlogical_result']
            result_arr = result_str.strip().split()
            save_model(
            	result_arr[1],
                request.user,
                result_arr[2],
                result_arr[3],
                result_arr[4],
                result_arr[5],
                result_arr[6],
                result_arr[7],
                result_arr[8],
                int(result_arr[9]),
                result_arr[10],
                result_arr[11],
                result_arr[12],
                result_arr[13],
                result_arr[14],
                result_arr[15],
                result_arr[16])
            form = PostForm()
            return render(request, 'evacalc/index.html', {"form": form,
                                                          'success': result_str})
    else:
        form = PostForm()
    return render(request, "evacalc/index.html", {'form': form})


def compute_skills_section(hard_skills, knowledge, soft_skills):
    """Практические занятия Управленческие знания Навыки взаимодействия"""

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
    """Область решаемых вопросов Сложность вопросов"""

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
    """ Свобода действий Природа воздействия Важность воздействия"""

    for arr in responsibility_arr:
        if str(arr[0]) == freedom_action:
            if str(arr[1]) == nature_impact:
                if str(arr[2]) == impact_importance:
                    return int(arr[3])
    return None


def grade_determine(sum_of_values):
    for summ in grade_arr:
        if (sum_of_values <= summ[2]) and (sum_of_values >= summ[1]):
            return summ[0]
    return None


def is_none(*args):
    for value in args:
        if value is None:
            return True
    return False


def is_waterfall_principle(hard_skills, around_question, freedom_action):
    if ord(hard_skills) < ord(around_question):
        return False
    elif ord(around_question) < ord(freedom_action):
        return False
    return True


def delete_job_evaluation(id, redirect_str):
    job_name = JobEvaluation.objects.get(id=id)
    job_name.delete()
    return redirect(redirect_str)

def returnexcel(request):

	"""Считывание с БД"""

	jobs_dicts = list(JobEvaluation.objects.filter(user=request.user).values())
	jobs_arr = []
	for dictionary in jobs_dicts:
		jobs_arr.append([])
		jobs_arr[-1].append(dictionary['title'])
		jobs_arr[-1].append(dictionary['short_profile'])
		jobs_arr[-1].append(dictionary['hard_skills'])
		jobs_arr[-1].append(dictionary['knowledge'])
		jobs_arr[-1].append(dictionary['soft_skills'])
		jobs_arr[-1].append(dictionary['value_of_skills_section'])
		jobs_arr[-1].append(dictionary['around_question'])
		jobs_arr[-1].append(dictionary['question_complexity'])
		jobs_arr[-1].append(dictionary['value_of_problems_section'])
		jobs_arr[-1].append(dictionary['value_of_union_section'])
		jobs_arr[-1].append(dictionary['freedom_action'])
		jobs_arr[-1].append(dictionary['nature_impact'])
		jobs_arr[-1].append(dictionary['impact_importance'])
		jobs_arr[-1].append(dictionary['value_of_responsibility_section'])
		jobs_arr[-1].append(dictionary['sum_of_values'])
		jobs_arr[-1].append(dictionary['grade'])
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = f'attachment; filename="{request.user}JobEvaluation.xlsx"'
	workbook = xlsxwriter.Workbook(response, {'in_memory': True})
	worksheet = workbook.add_worksheet('Список должностей')

	"""EPSI Заголовок"""

	epsi_header = workbook.add_format({
	'bold':True,
	'align':'center',
	'valign':'vcenter',
	'border':6,
	'color':"#FF0000",
	'fg_color':'DDDDDD',
	'font_name':'TimesNewRoman',
	'font_size': 22
	})
	worksheet.merge_range('B1:Z2', 'Калькулятор оценки должностей EPSI Rating', epsi_header)

	"""Заголовки ячеек"""

	cells_header = workbook.add_format({
		'bold':True,
		'text_wrap':True,
		'align':'vcenter',
		'valign':'center',
		'border':3,
		'color':'000000',
		'fg_color':'E41717',
		'font_name':'TimesNewRoman',
		'font_size':14,
		})

	titles_header = ["Название должности",
	"Краткий профиль",
    "Практические знания",
    "Управленческие знания",
    "Навыки общения",
    "Пункт оценки",
    "Область вопросов",
    "Сложность вопросов",
    "Значение в %",
    "Свобода действий",
    "Природа воздействия",
    "Важность воздействия",
    "Пункты оценки"]

	letter_numb = 65
	title_count = 0
	for _ in range(13):
		cell_title = titles_header[title_count]
		worksheet.merge_range(f'{chr(letter_numb)}3:{chr(letter_numb + 1)}4', f'{cell_title}', cells_header)
		letter_numb += 2
		title_count += 1
	worksheet.merge_range('AA3:AA4', 'Грейд', cells_header)

	"""Значения ячеек"""

	cells_values = workbook.add_format({
		'align':'vcenter',
		'valign':'center',
		'border':1,
		'color':'000000',
		'font_name':'TimesNewRoman',
		'font_size':14,
		})


	row_numb = 5
	for value in jobs_arr:
		col_numb = 65
		for each in range(13):
			worksheet.merge_range(f'{chr(col_numb)}{row_numb}:{chr(col_numb+1)}{row_numb}', f'{value[each]}', cells_values)
			col_numb += 2
		worksheet.write(f'AA{row_numb}', value[-1], cells_values)
		row_numb += 1
	workbook.close()
	return response

def save_model(*args):
	job_evaluation_save = JobEvaluation(
		title=args[0],
		user=args[1],
		short_profile=args[2],
		hard_skills=args[3],
		knowledge=args[4],
		soft_skills=args[5],
		value_of_skills_section=args[6],
		around_question=args[7],
		question_complexity=args[8],
		value_of_problems_section=int(args[9]),
		value_of_union_section=args[10],
		freedom_action=args[11],
		nature_impact=args[12],
		impact_importance=args[13],
		value_of_responsibility_section=args[14],
		sum_of_values=args[15],
		grade=args[16])
	job_evaluation_save.save()