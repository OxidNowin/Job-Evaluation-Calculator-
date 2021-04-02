from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import JobEvaluation
from .forms import (
    FirstSectionForm, SecondSectionForm, ThirdSectionForm,
    UnlogicalPostForm, SaveUnlogicalDictAndBack,AddInDBForm
    )
from .arrays import skills_arr, responsibility_arr, problems_solving_arr, union_arr, grade_arr

import xlsxwriter
import ast
from math import ceil

@login_required
def archive_date(request):
    if request.method == "POST" and 'delete_job' in request.POST:
        job_id = list(request.POST.values())[1]
        redirect_str = "archive_date"
        delete_job_evaluation(job_id, redirect_str)
    elif request.method == "POST" and 'recalculate' in request.POST:
        job_id = list(request.POST.values())[1]
        job = list(JobEvaluation.objects.filter(id=job_id).values())[0]
        job.pop('created_date')
        job_dict = {'title': job['title'],
                    'short_profile': job['short_profile'],
                    'hard_skills': job['hard_skills'],
                    'knowledge': job['knowledge'],
                    'soft_skills': job['soft_skills']}
        form = FirstSectionForm(job_dict)
        return render(request, 'evacalc/skills_section.html', {'form': form,
                                                                'job': job})
    elif request.method == "POST" and 'evaluate' in request.POST:
        form = FirstSectionForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data["job_input"]
            result_dict_1 = skills_operations(form)
            return render(request, 'evacalc/skills_section.html', {'form': form,
                                                                  'result_dict_1': result_dict_1,
                                                                  'job': job})
    elif request.method == 'POST' and 'next_step' in request.POST:
        form = FirstSectionForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            result_dict_1 = skills_operations(form)
            job_dict = {'around_question': job['around_question'],
                        'question_complexity': job['question_complexity']}
            form = SecondSectionForm(job_dict)
            if result_dict_1['is_skills_section_logical'] is False:
                return render(request, "evacalc/skills_section.html", {'form': form,
                                                                      'logical_message_1': 'Нелогичное сочетание!',
                                                                      'result_dict_1': result_dict_1,
                                                                      'job': job})
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_1':result_dict_1,
                                                                     'job': job})
    elif request.method == 'POST' and 'unlogical_post1' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_dict = {'around_question': job['around_question'],
                        'question_complexity': job['question_complexity']}
            result_dict_1 = form.cleaned_data['unlogical_result']
            form = SecondSectionForm(job_dict)
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_1':result_dict_1,
                                                                     'job': job})
    elif request.method=='POST' and 'evaluate2' in request.POST:
        form = SecondSectionForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data["job_input"]
            result_dict_1, result_dict_2 = problems_operations(form)   
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_2': result_dict_2,
                                                                      'result_dict_1': result_dict_1,
                                                                      'job': job})
    elif request.method=='POST' and 'next_step2' in request.POST:
        form = SecondSectionForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            result_dict_1, result_dict_2 = problems_operations(form)
            job_dict = {'freedom_action': job['freedom_action'],
                        'nature_impact': job['nature_impact'],
                        'impact_importance': job['impact_importance']}
            form = ThirdSectionForm(job_dict) 
            if (result_dict_2['is_problems_section_logical'] and result_dict_2['is_union_section_logical'] and
                result_dict_2['is_skills_section_logical']) is False:
                return render(request, "evacalc/problems_section.html", {'form': form,
                                                                         'logical_message_2': 'Нелогичное сочетание!',
                                                                         'result_dict_2': result_dict_2,
                                                                         'result_dict_1': result_dict_1,
                                                                         'job': job})
            return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'job': job})
    elif request.method == 'POST' and 'unlogical_post2' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_dict = {'freedom_action': job['freedom_action'],
                        'nature_impact': job['nature_impact'],
                        'impact_importance': job['impact_importance']}
            result_dict_2 = form.cleaned_data['unlogical_result']
            form = ThirdSectionForm(job_dict)
            return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'job': job})
    elif request.method=='POST' and 'go_to_2' in request.POST:
        form = SaveUnlogicalDictAndBack(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_dict = {'around_question': job['around_question'],
                        'question_complexity': job['question_complexity']}
            result_dict_1 = form.cleaned_data['back_dict']
            form = SecondSectionForm(job_dict)
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_1': result_dict_1,
                                                                     'job': job})
    elif request.method=='POST' and 'evaluate3' in request.POST:
        form = ThirdSectionForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data["job_input"]
            result_dict_2,result_dict_3 = responsibility_operations(form)   
            return render(request, 'evacalc/responsibility_section.html', {'form':form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'result_dict_3':result_dict_3,
                                                                           'job':job})
    elif request.method=='POST' and 'next_step3' in request.POST:
        form = ThirdSectionForm(request.POST)
        if form.is_valid():
            try:
                job = form.cleaned_data["job_input"]
                result_dict_2, result_dict_3 = responsibility_operations(form)
                grade_result_dict = grade_operations(result_dict_3)
            except Exception:
                return redirect('skills_section')
            else:
                return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                               'grade_result_dict': grade_result_dict,
                                                                               'job': job})
    elif request.method=="POST" and 'add_in_db' in request.POST:
        form = AddInDBForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_id = job['id']
            grade_result_dict = ast.literal_eval(form.cleaned_data['last_dict'])
            update_model(request.user, grade_result_dict, job_id)
            return redirect('archive_date')
    jobs_list = JobEvaluation.objects.order_by('-created_date').filter(user=request.user)
    context = {'jobs_list': jobs_list}
    return render(request, 'evacalc/archive.html', context)


@login_required
def archive_grade(request):
    if request.method == "POST" and 'delete_job' in request.POST:
        job_id = list(request.POST.values())[1]
        redirect_str = "archive_grade"
        delete_job_evaluation(job_id, redirect_str)
    elif request.method == "POST" and 'recalculate' in request.POST:
        job_id = list(request.POST.values())[1]
        job = list(JobEvaluation.objects.filter(id=job_id).values())[0]
        job.pop('created_date')
        job_dict = {'title': job['title'],
                    'short_profile': job['short_profile'],
                    'hard_skills': job['hard_skills'],
                    'knowledge': job['knowledge'],
                    'soft_skills': job['soft_skills']}
        form = FirstSectionForm(job_dict)
        return render(request, 'evacalc/skills_section.html', {'form': form,
                                                                'job': job})
    elif request.method == "POST" and 'evaluate' in request.POST:
        form = FirstSectionForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data["job_input"]
            result_dict_1 = skills_operations(form)
            return render(request, 'evacalc/skills_section.html', {'form': form,
                                                                  'result_dict_1': result_dict_1,
                                                                  'job': job})
    elif request.method == 'POST' and 'next_step' in request.POST:
        form = FirstSectionForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            result_dict_1 = skills_operations(form)
            job_dict = {'around_question': job['around_question'],
                        'question_complexity': job['question_complexity']}
            form = SecondSectionForm(job_dict)
            if result_dict_1['is_skills_section_logical'] is False:
                return render(request, "evacalc/skills_section.html", {'form': form,
                                                                      'logical_message_1': 'Нелогичное сочетание!',
                                                                      'result_dict_1': result_dict_1,
                                                                      'job': job})
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_1':result_dict_1,
                                                                     'job': job})
    elif request.method == 'POST' and 'unlogical_post1' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_dict = {'around_question': job['around_question'],
                        'question_complexity': job['question_complexity']}
            result_dict_1 = form.cleaned_data['unlogical_result']
            form = SecondSectionForm(job_dict)
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_1':result_dict_1,
                                                                     'job': job})
    elif request.method=='POST' and 'evaluate2' in request.POST:
        form = SecondSectionForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data["job_input"]
            result_dict_1, result_dict_2 = problems_operations(form)   
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_2': result_dict_2,
                                                                      'result_dict_1': result_dict_1,
                                                                      'job': job})
    elif request.method=='POST' and 'next_step2' in request.POST:
        form = SecondSectionForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            result_dict_1, result_dict_2 = problems_operations(form)
            job_dict = {'freedom_action': job['freedom_action'],
                        'nature_impact': job['nature_impact'],
                        'impact_importance': job['impact_importance']}
            form = ThirdSectionForm(job_dict) 
            if (result_dict_2['is_problems_section_logical'] and result_dict_2['is_union_section_logical'] and
                result_dict_2['is_skills_section_logical']) is False:
                return render(request, "evacalc/problems_section.html", {'form': form,
                                                                         'logical_message_2': 'Нелогичное сочетание!',
                                                                         'result_dict_2': result_dict_2,
                                                                         'result_dict_1': result_dict_1,
                                                                         'job': job})
            return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'job': job})
    elif request.method == 'POST' and 'unlogical_post2' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_dict = {'freedom_action': job['freedom_action'],
                        'nature_impact': job['nature_impact'],
                        'impact_importance': job['impact_importance']}
            result_dict_2 = form.cleaned_data['unlogical_result']
            form = ThirdSectionForm(job_dict)
            return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'job': job})
    elif request.method=='POST' and 'go_to_2' in request.POST:
        form = SaveUnlogicalDictAndBack(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_dict = {'around_question': job['around_question'],
                        'question_complexity': job['question_complexity']}
            result_dict_1 = form.cleaned_data['back_dict']
            form = SecondSectionForm(job_dict)
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_1': result_dict_1,
                                                                     'job': job})
    elif request.method=='POST' and 'evaluate3' in request.POST:
        form = ThirdSectionForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data["job_input"]
            result_dict_2,result_dict_3 = responsibility_operations(form)   
            return render(request, 'evacalc/responsibility_section.html', {'form':form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'result_dict_3':result_dict_3,
                                                                           'job':job})
    elif request.method=='POST' and 'next_step3' in request.POST:
        form = ThirdSectionForm(request.POST)
        if form.is_valid():
            try:
                job = form.cleaned_data["job_input"]
                result_dict_2, result_dict_3 = responsibility_operations(form)
                grade_result_dict = grade_operations(result_dict_3)
            except Exception:
                return redirect('skills_section')
            else:
                return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                               'grade_result_dict': grade_result_dict,
                                                                               'job': job})
    elif request.method=="POST" and 'add_in_db' in request.POST:
        form = AddInDBForm(request.POST)
        if form.is_valid():
            job = ast.literal_eval(form.cleaned_data["job_input"])
            job_id = job['id']
            grade_result_dict = ast.literal_eval(form.cleaned_data['last_dict'])
            update_model(request.user, grade_result_dict, job_id)
            return redirect('archive_date')
    jobs_list = JobEvaluation.objects.order_by('-grade').filter(user=request.user)
    context = {'jobs_list': jobs_list}
    return render(request, 'evacalc/archive.html', context)


@login_required
def skills_section(request):
    if request.method == "POST" and 'evaluate' in request.POST:
        form = FirstSectionForm(request.POST)
        if form.is_valid():
            result_dict_1 = skills_operations(form)
            return render(request, 'evacalc/skills_section.html', {'form': form,
                                                                  'result_dict_1': result_dict_1,})
    elif request.method == 'POST' and 'next_step' in request.POST:
        form = FirstSectionForm(request.POST)
        if form.is_valid():
            result_dict_1 = skills_operations(form)
            if result_dict_1['is_skills_section_logical'] is False:
                return render(request, "evacalc/skills_section.html", {'form': form,
                                                                      'logical_message_1': 'Нелогичное сочетание!',
                                                                      'result_dict_1': result_dict_1})
            return render(request, 'evacalc/problems_section.html', {'form': SecondSectionForm(),
                                                                     'result_dict_1':result_dict_1})
    elif request.method == 'POST' and 'unlogical_post1' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            result_dict_1 = form.cleaned_data['unlogical_result']
            return render(request, 'evacalc/problems_section.html', {'form': SecondSectionForm(),
                                                                     'result_dict_1':result_dict_1,})
    elif request.method=='POST' and 'evaluate2' in request.POST:
        form = SecondSectionForm(request.POST)
        if form.is_valid():
            result_dict_1, result_dict_2 = problems_operations(form)   
            return render(request, 'evacalc/problems_section.html', {'form': form,
                                                                     'result_dict_2': result_dict_2,
                                                                      'result_dict_1': result_dict_1})
    elif request.method=='POST' and 'next_step2' in request.POST:
        form = SecondSectionForm(request.POST)
        if form.is_valid():
            result_dict_1, result_dict_2 = problems_operations(form) 
            if (result_dict_2['is_problems_section_logical'] and result_dict_2['is_union_section_logical'] and
                result_dict_2['is_skills_section_logical']) is False:
                return render(request, "evacalc/problems_section.html", {'form': form,
                                                                         'logical_message_2': 'Нелогичное сочетание!',
                                                                         'result_dict_2': result_dict_2,
                                                                         'result_dict_1': result_dict_1,})
            return render(request, 'evacalc/responsibility_section.html', {'form': ThirdSectionForm(),
                                                                           'result_dict_2':result_dict_2,})
    elif request.method == 'POST' and 'unlogical_post2' in request.POST:
        form = UnlogicalPostForm(request.POST)
        if form.is_valid():
            result_dict_2 = form.cleaned_data['unlogical_result']
            return render(request, 'evacalc/responsibility_section.html', {'form': ThirdSectionForm(),
                                                                           'result_dict_2':result_dict_2,})
    elif request.method=='POST' and 'go_to_2' in request.POST:
        form = SaveUnlogicalDictAndBack(request.POST)
        if form.is_valid():
            result_dict_1 = form.cleaned_data['back_dict']
            return render(request, 'evacalc/problems_section.html', {'form': SecondSectionForm(),
                                                                     'result_dict_1': result_dict_1})
    elif request.method=='POST' and 'evaluate3' in request.POST:
        form = ThirdSectionForm(request.POST)
        if form.is_valid():
            result_dict_2,result_dict_3 = responsibility_operations(form)   
            return render(request, 'evacalc/responsibility_section.html', {'form':form,
                                                                           'result_dict_2':result_dict_2,
                                                                           'result_dict_3':result_dict_3})
    elif request.method=='POST' and 'next_step3' in request.POST:
        form = ThirdSectionForm(request.POST)
        if form.is_valid():
            try:
                result_dict_2, result_dict_3 = responsibility_operations(form)
                grade_result_dict = grade_operations(result_dict_3)
            except Exception:
                return redirect('skills_section')
            else:
                return render(request, 'evacalc/responsibility_section.html', {'form': form,
                                                                               'grade_result_dict': grade_result_dict,})
    elif request.method=="POST" and 'add_in_db' in request.POST:
        form = AddInDBForm(request.POST)
        if form.is_valid():
            grade_result_dict = ast.literal_eval(form.cleaned_data['last_dict'])
            save_model(request.user, grade_result_dict)
            return redirect('archive_date')
    else:
        form = FirstSectionForm()
    return render(request, 'evacalc/skills_section.html', {'form':form})


def skills_operations(form):
    title = form.cleaned_data['title'].title()
    short_profile = form.cleaned_data['short_profile'].upper()
    hard_skills = str(form.cleaned_data['hard_skills'].upper())
    knowledge = str(form.cleaned_data['knowledge'].upper())
    soft_skills = str(form.cleaned_data['soft_skills'].upper())

    value_of_skills_section, is_skills_section_logical = compute_skills_section(hard_skills, knowledge,
                                                                                        soft_skills)

    result_dict_1 = {'title': title,
                     'short_profile': short_profile,
                     'hard_skills': hard_skills,
                     'knowledge': knowledge,
                     'soft_skills': soft_skills,
                     'value_of_skills_section': value_of_skills_section,
                     'is_skills_section_logical': is_skills_section_logical,}

    return result_dict_1


def problems_operations(form):
    result_dict_1 = ast.literal_eval(form.cleaned_data['result_dict_1'])
    around_question = str(form.cleaned_data['around_question'].upper())
    question_complexity = str(form.cleaned_data['question_complexity'].upper())
    value_of_skills_section = result_dict_1['value_of_skills_section']
    value_of_problems_section, is_problems_section_logical = compute_problems_section(around_question, question_complexity)
    value_of_union_section, is_union_section_logical = compute_union_skills_and_problems(value_of_skills_section, 
                                                                                            value_of_problems_section)
    value_of_problems_section = int(ceil(value_of_problems_section*100))
    result_dict_2 = result_dict_1.copy()
    result_dict_2.update({'around_question': around_question,
                          'question_complexity': question_complexity,
                          'value_of_problems_section': value_of_problems_section,
                          'value_of_union_section': value_of_union_section,
                          'is_problems_section_logical': is_problems_section_logical,
                          'is_union_section_logical': is_union_section_logical,})
    return result_dict_1, result_dict_2


def responsibility_operations(form):
    result_dict_2 = ast.literal_eval(form.cleaned_data['grade_result_dict'])
    freedom_action = str(form.cleaned_data['freedom_action'].upper())
    nature_impact = str(form.cleaned_data['nature_impact'].upper())
    impact_importance = str(form.cleaned_data['impact_importance'].upper())

    value_of_responsibility_section = compute_responsibility_section(freedom_action, nature_impact, impact_importance)

    result_dict_3 = result_dict_2.copy()
    result_dict_3.update({'freedom_action': freedom_action,
                          'nature_impact': nature_impact,
                          'impact_importance': impact_importance,
                          'value_of_responsibility_section': value_of_responsibility_section})

    return result_dict_2, result_dict_3


def grade_operations(result_dict_3):
    value_of_skills_section = int(result_dict_3['value_of_skills_section'])
    value_of_union_section = int(result_dict_3['value_of_union_section'])
    value_of_responsibility_section = int(result_dict_3['value_of_responsibility_section'])
    sum_of_values = value_of_skills_section + value_of_union_section + value_of_responsibility_section
    grade = grade_determine(sum_of_values)
    result_dict = result_dict_3.copy()
    result_dict.update({'sum_of_values': sum_of_values,
                        'grade': grade})
    return result_dict


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
    is_union_section_logical = True

    for arr in union_arr:
        if str(arr[0]) == str(value_of_problems_section):
            if str(arr[1]) == str(value_of_skills_section):
                if str(arr[3]) == "0":
                    is_union_section_logical = False
                return int(arr[2]), is_union_section_logical
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


def delete_job_evaluation(id, redirect_str):
    job = JobEvaluation.objects.get(id=id)
    job.delete()
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
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'border': 6,
        'color': "#000000",
        'fg_color': '#FFFFFF',
        'font_name': 'TimesNewRoman',
        'font_size': 16
    })
    worksheet.merge_range('B1:Z2', 'Калькулятор оценки должностей EPSI Rating', epsi_header)

    """Заголовки ячеек"""

    cells_header = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'align': 'vcenter',
        'valign': 'center',
        'border': 3,
        'color': '#000000',
        'fg_color': 'D0D0D0',
        'font_name': 'TimesNewRoman',
        'font_size': 14,
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
                     "Значение оценки",
                     "Свобода действий",
                     "Природа воздействия",
                     "Важность воздействия"
                     ]

    letter_numb = 65
    title_count = 0
    for _ in range(13):
        cell_title = titles_header[title_count]
        worksheet.merge_range(f'{chr(letter_numb)}3:{chr(letter_numb + 1)}4', f'{cell_title}', cells_header)
        letter_numb += 2
        title_count += 1
    worksheet.merge_range('AA3:AB4', 'Пункты оценки', cells_header)
    worksheet.merge_range('AC3:AC4', 'Сумма оценок', cells_header)
    worksheet.merge_range('AD3:AD4', 'Грейд', cells_header)

    """Значения ячеек"""

    cells_values = workbook.add_format({
        'align': 'vcenter',
        'valign': 'center',
        'border': 1,
        'color': '000000',
        'font_name': 'TimesNewRoman',
        'font_size': 12,
    })

    row_numb = 5
    for value in jobs_arr:
        col_numb = 65
        for each in range(13):
            worksheet.merge_range(f'{chr(col_numb)}{row_numb}:{chr(col_numb + 1)}{row_numb}', f'{value[each]}',cells_values)
            col_numb += 2
        worksheet.merge_range(f'AA{row_numb}:AB{row_numb}', value[-3], cells_values)
        worksheet.write(f'AC{row_numb}', value[-2], cells_values)
        worksheet.write(f'AD{row_numb}', value[-1], cells_values)
        row_numb += 1
    workbook.close()
    return response


def save_model(username, grade_dict):
    job_evaluation_save = JobEvaluation(
        title = grade_dict['title'],
        user = username,
        short_profile = grade_dict['short_profile'],
        hard_skills = grade_dict['hard_skills'],
        knowledge = grade_dict['knowledge'],
        soft_skills = grade_dict['soft_skills'],
        value_of_skills_section = grade_dict['value_of_skills_section'],
        around_question = grade_dict['around_question'],
        question_complexity = grade_dict['question_complexity'],
        value_of_problems_section = int(grade_dict['value_of_problems_section']),
        value_of_union_section = grade_dict['value_of_union_section'],
        freedom_action = grade_dict['freedom_action'],
        nature_impact = grade_dict['nature_impact'],
        impact_importance = grade_dict['impact_importance'],
        value_of_responsibility_section = grade_dict['value_of_responsibility_section'],
        sum_of_values = grade_dict['sum_of_values'],
        grade = grade_dict['grade'])
    job_evaluation_save.save()


def update_model(username, grade_dict, job_id):
    job_update = JobEvaluation(
        id = job_id,
        title = grade_dict['title'],
        user = username,
        short_profile = grade_dict['short_profile'],
        hard_skills = grade_dict['hard_skills'],
        knowledge = grade_dict['knowledge'],
        soft_skills = grade_dict['soft_skills'],
        value_of_skills_section = grade_dict['value_of_skills_section'],
        around_question = grade_dict['around_question'],
        question_complexity = grade_dict['question_complexity'],
        value_of_problems_section = int(grade_dict['value_of_problems_section']),
        value_of_union_section = grade_dict['value_of_union_section'],
        freedom_action = grade_dict['freedom_action'],
        nature_impact = grade_dict['nature_impact'],
        impact_importance = grade_dict['impact_importance'],
        value_of_responsibility_section = grade_dict['value_of_responsibility_section'],
        sum_of_values = grade_dict['sum_of_values'],
        grade = grade_dict['grade'])
    job_update.save()