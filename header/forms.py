from django import forms

from header.models import QuestionsModel, ReviewsModel


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionsModel
        fields = ['title', 'question']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewsModel
        fields = ['username', 'avatar', 'review']

