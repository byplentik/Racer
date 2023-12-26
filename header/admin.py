from django.contrib import admin

from header.models import QuestionsModel, ReviewsModel


@admin.register(QuestionsModel)
class AdminQuestionsModel(admin.ModelAdmin):
    list_display = ['title', 'question', 'answered']


@admin.register(ReviewsModel)
class AdminReviewsModel(admin.ModelAdmin):
    list_display = ['created_at', 'username']