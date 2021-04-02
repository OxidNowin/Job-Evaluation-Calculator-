from django import forms
from django.utils import timezone

profile_choices = [('', 'Краткий профиль'),
                   ('P4', 'P4'), ('P3', 'P3'),
                   ('P2', 'P2'), ('P1', 'P1'),
                   ('L', 'L'), ('A1', 'A1'),
                   ('A2', 'A2'), ('A3', 'A3'),
                   ('A4', 'A4')]

hard_skills_choices = [('', '-'),
                       ('A', 'A'), ('B', 'B'),
                       ('C', 'C'), ('D', 'D'),
                       ('E', 'E'), ('F', 'F'),
                       ('G', 'G'), ('H', 'H')]

knowledge_choices = [('', '-'), ('T', 'T'),
                     ('I', 'I'), ('II', 'II'),
                     ('III', 'III'), ('IV', 'IV')]

soft_skills_choices = [('', '-'), ('1', '1'),
                       ('2', '2'), ('3', '3')]

around_question_choices = [('', '-'),
                           ('A', 'A'), ('B', 'B'),
                           ('C', 'C'), ('D', 'D'),
                           ('E', 'E'), ('F', 'F'),
                           ('G', 'G'), ('H', 'H')]

question_complexity_choices = [('', '-'),
                               ('1', '1'), ('2', '2'),
                               ('3', '3'), ('4', '4'),
                               ('5', '5')]

freedom_action_choices = [('', '-'),
                          ('A', 'A'), ('B', 'B'),
                          ('C', 'C'), ('D', 'D'),
                          ('E', 'E'), ('F', 'F'),
                          ('G', 'G'), ('H', 'H')]

nature_impact_choices = [('', '-'), ('N', 'N'),
                         ('1', '1'), ('2', '2'),
                         ('3', '3'), ('4', '4'), ]

impact_importance_choices = [('', '-'),
                             ('R', 'R'), ('C', 'C'),
                             ('S', 'S'), ('P', 'P'),
                             ('I', 'I'),
                             ('II', 'II'), ('III', 'III'),
                             ('IV', 'IV')]


class FirstSectionForm(forms.Form):
  title = forms.CharField(label="Название должности", max_length=250)
  short_profile = forms.ChoiceField(widget=forms.Select, choices=profile_choices)
  hard_skills = forms.ChoiceField(widget=forms.Select, choices=hard_skills_choices)
  knowledge = forms.ChoiceField(widget=forms.Select, choices=knowledge_choices)
  soft_skills = forms.ChoiceField(widget=forms.Select, choices=soft_skills_choices)
  job_input = forms.CharField()

  def __init__(self, *args, **kwargs):
        super(FirstSectionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs={
            'placeholder': 'Введите название должности'}


class SecondSectionForm(forms.Form):
  result_dict_1 = forms.CharField(label="result_dict_1")
  around_question = forms.ChoiceField(widget=forms.Select, choices=around_question_choices)
  question_complexity = forms.ChoiceField(widget=forms.Select, choices=question_complexity_choices)
  job_input = forms.CharField()


class ThirdSectionForm(forms.Form):
  grade_result_dict = forms.CharField(label="grade_result_dict")
  freedom_action = forms.ChoiceField(widget=forms.Select, choices=freedom_action_choices)
  nature_impact = forms.ChoiceField(widget=forms.Select, choices=nature_impact_choices)
  impact_importance = forms.ChoiceField(widget=forms.Select, choices=impact_importance_choices)
  job_input = forms.CharField()


class UnlogicalPostForm(forms.Form):
  unlogical_result = forms.CharField(label="unlogical_result")
  job_input = forms.CharField()


class SaveUnlogicalDictAndBack(forms.Form):
  back_dict = forms.CharField(label="back_dict")
  job_input = forms.CharField()


class AddInDBForm(forms.Form):
  last_dict = forms.CharField(label="last_dict")
  job_input = forms.CharField()

class Authorization(forms.Form):
  username = forms.CharField(label="username")
  password = forms.CharField(label="password")
    