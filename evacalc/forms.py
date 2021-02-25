from django import forms

from .models import JobEvaluation

class PostForm(forms.ModelForm):
	
	class Meta:
		model = JobEvaluation
		fields = ("title", "tech_skills", 
				"knowledge", "soft_skills",
				"around_question", "question_diff",
				"free_move", "nature", "impact_importance",)

class UnlogicalPostForm(forms.Form):
	dict = forms.CharField(label="dict")