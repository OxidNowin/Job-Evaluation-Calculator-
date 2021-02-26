from django import forms

from .models import JobEvaluation

class PostForm(forms.ModelForm):
	
	class Meta:
		model = JobEvaluation
		fields = ("title", "short_profile", 
				"tech_skills", 
				"knowledge", "soft_skills",
				"around_question", "question_diff",
				"free_move", "nature", "impact_importance",)

class UnlogicalPostForm(forms.Form):
	unlogical_result = forms.CharField(label="unlogical_result")