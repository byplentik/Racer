from django.contrib import admin

from header.models import QuestionsModel


@admin.register(QuestionsModel)
class AdminQuestionsModel(admin.ModelAdmin):
    list_display = ['title', 'question', 'answered']