from django import forms

profile_choices=[('','Краткий профиль'),
				('P4','P4'),('P3','P3'),
				('P2','P2'),('P1','P1'),
				('L','L'),('A1','A1'),
				('A2','A2'),('A3','A3'),
				('A4','A4')]

tech_skills_choices=[('-','-'),
					('A','A'),('B','B'),
					('C','C'),('D','D'),
					('E','E'),('F','F'),
					('G','G'),('H','H')]

knowledge_choices=[('-','-'),('T','T'),
					('I','I'),('II','II'),
					('III','III'),('IV','IV')]

soft_skills_choices=[('-','-'),('1','1'),
					('2','2'),('3','3')]

around_question_choices=[('-','-'),
						('A','A'),('B','B'),
						('C','C'),('D','D'),
						('E','E'),('F','F'),
						('G','G'),('H','H')]

question_diff_choices=[('-','-'),
					('1','1'),('2','2'),
					('3','3'),('4','4'),
					('5','5')]

free_move_choices=[('-','-'),
					('A','A'),('B','B'),
					('C','C'),('D','D'),
					('E','E'),('F','F'),
					('G','G'),('H','H')]

nature_choices=[('-','-'),('N','N'),
				('1','1'),('2','2'),
				('3','3'),('4','4'),]

impact_importance_choices=[('-','-'),
						('R','R'),('C','C'),
						('S','S'),('P','P'),
						('I','I'),
						('II','II'),('III','III'),
						('IV','IV')]

class PostForm(forms.Form):
	title = forms.CharField(max_length=25)
	short_profile = forms.ChoiceField(widget=forms.Select,choices=profile_choices) 
	tech_skills = forms.ChoiceField(widget=forms.Select,choices=tech_skills_choices)
	knowledge = forms.ChoiceField(widget=forms.Select,choices=knowledge_choices)
	soft_skills = forms.ChoiceField(widget=forms.Select,choices=soft_skills_choices)
	around_question = forms.ChoiceField(widget=forms.Select,choices=around_question_choices)
	question_diff = forms.ChoiceField(widget=forms.Select,choices=question_diff_choices)
	free_move = forms.ChoiceField(widget=forms.Select,choices=free_move_choices)
	nature = forms.ChoiceField(widget=forms.Select,choices=nature_choices)
	impact_importance = forms.ChoiceField(widget=forms.Select,choices=impact_importance_choices)

class UnlogicalPostForm(forms.Form):
	unlogical_result = forms.CharField(label="unlogical_result")