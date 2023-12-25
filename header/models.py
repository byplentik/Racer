from django.db import models


class QuestionsModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название вопроса (Тема)')
    question = models.TextField(verbose_name='Вопрос')
    response = models.TextField(verbose_name='Ответ', blank=True)
    answered = models.BooleanField(default=False, verbose_name='Ответить')

    def __str__(self):
        return str(self.title)