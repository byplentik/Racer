from django import forms

from header.models import QuestionsModel, ReviewsModel


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionsModel
        fields = ['title', 'question']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewsModel
        fields = ['username', 'avatar', 'review']

