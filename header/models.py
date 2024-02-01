from django.db import models


class QuestionsModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название вопроса (Тема)')
    question = models.TextField(verbose_name='Вопрос')
    response = models.TextField(verbose_name='Ответ', blank=True)
    answered = models.BooleanField(default=False, verbose_name='Ответить')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return str(self.title)


class ReviewsModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    username = models.CharField(max_length=255, verbose_name='Имя пользователя')
    avatar = models.ImageField(upload_to='images_avatars/', verbose_name='Аватар')
    review = models.TextField(verbose_name='Отзыв')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.username)
