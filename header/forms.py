from django import forms

from header.models import QuestionsModel


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionsModel
        fields = ['title', 'question']